#!/usr/bin/env python3

import aws_cdk as cdk

from resume_api_gw.resume_api_gw_stack import ResumeApiGwStack


app = cdk.App()
ResumeApiGwStack(app, "ResumeApiGwStack", synthesizer=cdk.DefaultStackSynthesizer(generate_bootstrap_version_rule=False)
    )
app.synth()
