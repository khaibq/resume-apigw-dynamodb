from aws_cdk import (
    Stack,
    CfnOutput,
    aws_dynamodb,
    aws_apigateway,
    aws_iam
)
from constructs import Construct

class ResumeApiGwStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # Create DynamoDB table with partition key:id, type:string, provision read/write:1
        resume_dynamodb = aws_dynamodb.Table(self, "resumeTable",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PROVISIONED,
            read_capacity=1,
            write_capacity=1
        )
        resume_api = aws_apigateway.RestApi(self, 'resumeApiGW',
            endpoint_types=[aws_apigateway.EndpointType.REGIONAL],
            default_method_options=aws_apigateway.MethodOptions(
                method_responses=[aws_apigateway.MethodResponse(
                    status_code="200"
                )]
            )
        )
        getputitem_apigw_policy = aws_iam.Policy(self, "GetPutItemApiGWPolicy",
            statements=[aws_iam.PolicyStatement(
                actions=["dynamodb:GetItem", "dynamodb:PutItem"],
                effect=aws_iam.Effect.ALLOW,
                resources=[resume_dynamodb.table_arn]
            )]
        )
        getputitem_apigw_role = aws_iam.Role(self, "GetPutItemApiGWRole",
            assumed_by=aws_iam.ServicePrincipal("apigateway.amazonaws.com")
        )
        getputitem_apigw_role.attach_inline_policy(getputitem_apigw_policy)

        # Read mapping template - GET
        get_integration_request = open("./integration/get_integration_request", "r")
        get_integration_request_read = get_integration_request.read()
        get_integration_request.close()
        get_integration_response = open("./integration/get_integration_response", "r")
        get_integration_response_read = get_integration_response.read()
        get_integration_response.close()

        getitem_aws_integration = aws_apigateway.AwsIntegration(
            service="dynamodb",
            action="GetItem",
            options=aws_apigateway.IntegrationOptions(
                credentials_role=getputitem_apigw_role,
                passthrough_behavior=aws_apigateway.PassthroughBehavior.WHEN_NO_TEMPLATES,
                request_templates={"application/json": get_integration_request_read},
                integration_responses=[aws_apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={"method.response.header.Access-Control-Allow-Origin": "'*'"},
                    response_templates={"application/json": get_integration_response_read}
                )]
            )
        )

        # Read mapping template - PUT
        put_integration_request = open("./integration/put_integration_request", "r")
        put_integration_request_read = put_integration_request.read()
        put_integration_request.close()

        putitem_aws_integration = aws_apigateway.AwsIntegration(
            service="dynamodb",
            action="PutItem",
            options=aws_apigateway.IntegrationOptions(
                credentials_role=getputitem_apigw_role,
                passthrough_behavior=aws_apigateway.PassthroughBehavior.WHEN_NO_TEMPLATES,
                request_templates={"application/json": put_integration_request_read},
                integration_responses=[aws_apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={"method.response.header.Access-Control-Allow-Origin": "'*'"})]
            )
        )
        get_method_response = [aws_apigateway.MethodResponse(
            status_code="200",
            response_parameters={"method.response.header.Access-Control-Allow-Origin": True}
        )]
        resume_api.root.add_method("GET",
            integration=getitem_aws_integration,
            method_responses=get_method_response
        )

        post_method_response = [aws_apigateway.MethodResponse(
            status_code="200",
            response_parameters={"method.response.header.Access-Control-Allow-Origin": True}
        )]
        resume_api.root.add_method("POST",
            integration=putitem_aws_integration,
            method_responses=post_method_response
        )
        CfnOutput(self, "TableName", value=resume_dynamodb.table_name)
        CfnOutput(self, "APIUrl", value=resume_api.url)

