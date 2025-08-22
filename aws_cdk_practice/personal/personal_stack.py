from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_s3_notifications as s3_notifications,
    RemovalPolicy

)
import aws_cdk as cdk
from constructs import Construct

class PersonalStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "PersonalQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        bucket = s3.Bucket(
            self, 
            "MyS3Bucket",
            bucket_name="sidd-cdk-s3-buck-245024",  # Change this to your desired bucket name
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,  # Use RETAIN for production
            auto_delete_objects=True,  # Only use in development/testing
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="DeleteOldVersions",
                    enabled=True,
                    noncurrent_version_expiration=Duration.days(2)
                )
            ]
        )
         # L2 SNS Topic - Much simpler
        topic = sns.Topic(
            self, "sns_notification_topic_sidd_cdk",
            display_name="S3 Upload Notifications"
        )

        # L2 Email Subscription - One line!
        topic.add_subscription(
            subscriptions.EmailSubscription("sidd.245@gmail.com")
        )
        
        # L2 S3 Notification - Automatic IAM policies!
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.SnsDestination(topic)
        )

        # Output the bucket name and ARN
        cdk.CfnOutput(
            self, 
            "BucketName",
            value=bucket.bucket_name,
            description="Name of the created S3 bucket"
        )
        
        cdk.CfnOutput(
            self, 
            "BucketArn",
            value=bucket.bucket_arn,
            description="ARN of the created S3 bucket"
        )
