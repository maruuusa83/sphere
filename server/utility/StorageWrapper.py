# coding: utf-8
"""
各種便利なクラスを色々放り込んでおきます
"""
__author__ = u"Daichi Teruya"

import boto3

class StorageWrapper:
    """
    ストレージにアクセスするためのラッパです
    """

    __BUCKET_NAME       = u''
    __ACCESS_KEY_ID     = u''
    __SECRET_ACCESS_KEY = u''
    __S3_HOST_NAME      = u''
    __REGION_NAME       = u''
    __UPLOAD_DIR        = u''

    def __new__(cls, *argc, **argv):
        """
        シングルトンにするための処理を書いています
        """
        if not hasattr(cls, "__instance"):
            cls.__instance = super().__new__(cls, *argc, **argv)
        return cls.__instance

    def __init__(self, *argc, **argv):
        """
        S3へのアクセスで必要な処理を行っています
        """
        self.__session = boto3.session.Session(
                           region_name = self.__REGION_NAME,
                           aws_access_key_id = self.__ACCESS_KEY_ID,
                           aws_secret_access_key = self.__SECRET_ACCESS_KEY)
        self.__s3 = self.__session.resource('s3')
        self.__bucket = self.__s3.Bucket(self.__BUCKET_NAME)
        return

    def put_image(self, name, data):
        """
        dataに渡したイメージを、ファイル名をnameとしてS3上に保存します
        @param self
        @param name utf-8形式のファイル名
        @param data バイナリ形式の画像ファイル
        @return http://boto3.readthedocs.org/en/latest/reference/services/s3.html#S3.Object.put のReturnsの項参照
        """
        obj = self.__bucket.Object(self.__UPLOAD_DIR + name)
        response = obj.put(Body=data, ContentType='image/jpeg')
        return response

