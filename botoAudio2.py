# -*- coding: utf-8 -*-

import hashlib

import boto3

from aws import KEYS
    AWS_ACCESS_KEY_ID = KEYS.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = KEYS.AWS_SECRET_ACCESS_KEY

class ETSManager:
    """
        @todo: manages and provides the ets services
    """
    preset_ids = {
        'hls-2000k': '1351620000001-200010',
        'hls-1500k': '1351620000001-200020',
        'hls-1000k': '1351620000001-200030'
    }

    segment_duration = '4'

    def __init__(self):
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
        self.client = session.client('elastictranscoder', 'eu-west-1')



        response = self.client.create_pipeline(
            Name='bPipe',
            InputBucket='workplace-lms2',
            OutputBucket='workplace-lms2',
            Role='string',
            AwsKmsKeyArn='string',
            Notifications={
                'Progressing': 'string',
                'Completed': 'string',
                'Warning': 'string',
                'Error': 'string'
            },
            ContentConfig={
                'Bucket': 'string',
                'StorageClass': 'string',
                'Permissions': [
                    {
                        'GranteeType': 'string',
                        'Grantee': 'string',
                        'Access': [
                            'string',
                        ]
                    },
                ]
            },
            ThumbnailConfig={
                'Bucket': 'string',
                'StorageClass': 'string',
                'Permissions': [
                    {
                        'GranteeType': 'string',
                        'Grantee': 'string',
                        'Access': [
                            'string',
                        ]
                    },
                ]
            }
        )


    def transcode_hls(self, pipeline_id, input_key, output_key_prefix):
        """
        Args:
            pipeline_id: id of pipeline for transcoding video for hls
            input_key: uploaded video key (video is stored in S3)
            output_key_prefix: prefix of directory of filename for m3u file
        Returns:
            m3u8 file key of playlist
        """
        output_key = hashlib.sha256(input_key.encode('utf-8')).hexdigest()

        input = {
            'Key': input_key
        }

        hls_2000k = {
            'Key': 'hls2000k/' + output_key,
            'ThumbnailPattern': 'hls2000k/thumbnail/' + output_key + '-{resolution}-{count}',
            'PresetId': self.preset_ids['hls-2000k'],
            'SegmentDuration': self.segment_duration
        }

        hls_1500k = {
            'Key': 'hls1500k/' + output_key,
            'ThumbnailPattern': 'hls1500k/thumbnail/' + output_key + '-{resolution}-{count}',
            'PresetId': self.preset_ids['hls-1500k'],
            'SegmentDuration': self.segment_duration
        }

        hls_1000k = {
            'Key': 'hls1000k/' + output_key,
            'ThumbnailPattern': 'hls1000k/thumbnail/' + output_key + '-{resolution}-{count}',
            'PresetId': self.preset_ids['hls-1000k'],
            'SegmentDuration': self.segment_duration
        }

        outputs = [
            hls_2000k, hls_1500k, hls_1000k
        ]

        playlists = [
            {
                'Name': 'hls_' + output_key,
                'Format': 'HLSv3',
                'OutputKeys': [
                    hls_2000k['Key'], hls_1500k['Key'], hls_1000k['Key']
                ],
                'HlsContentProtection': {
                    'Method': 'aes-128',
                    'KeyStoragePolicy': 'WithVariantPlaylists'
                }
            }
        ]

        job_result = self.client.create_job(PipelineId=pipeline_id,
                                          Input=input,
                                          Outputs=outputs,
                                          OutputKeyPrefix=output_key_prefix + output_key + '/',
                                          Playlists=playlists)

        return '/'.join([output_key, job_result['Job']['Playlists'][0]['Name'] + '.m3u8'])