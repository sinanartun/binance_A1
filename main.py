import asyncio
import time
import datetime
import os

from binance import AsyncClient, BinanceSocketManager

from boto3.session import Session


AccessKeyId = os.getenv('AccessKeyId')
SecretAccessKey = os.getenv('SecretAccessKey')
bucket_name = os.getenv('bucket_name')
region = os.getenv('region')


session = Session(aws_access_key_id=AccessKeyId,
                  aws_secret_access_key=SecretAccessKey,
                  region_name=region)
s3 = session.resource('s3')

bucket = s3.Bucket(bucket_name)


def upload_file(local_data_file_path, remote_data_file_path):
    print(local_data_file_path, remote_data_file_path)
    s3.meta.client.upload_file(Filename=local_data_file_path, Bucket=bucket_name, Key=remote_data_file_path)


async def main():
    active_file_time = int(round(time.time()) / 60)
    new_local_data_file_path = './data/' + str(int(active_file_time * 60)) + '.tsv'

    f = open(new_local_data_file_path, 'w')
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    trade_socket = bm.trade_socket('BTCUSDT')
    # BTCUSDT parametresindeki market hareketlerinin datasını istiyoruz.
    async with trade_socket as tscm:
        while True:
            res = await tscm.recv()
            new_file_time = int(res['T'] / (1000 * 60))
            # Gelen datanın içindeki unixtime'ı (milisecond cinsinden) dakikaya çeviriyoruz.
            print(res)
            if new_file_time != active_file_time:
                f.close()
                # Eğer mesajın içindeki Unix dakikası active_file_time'a eşit değil ise 1dk'lık biriktirme süresi,
                # dolmuş ve biriktirilen datanın bucket'a yüklenmesi gerekli.
                local_data_file_path = './data/' + str(active_file_time * 60) + '.tsv'
                remote_data_file_path = 'data_1_min/' + str(active_file_time * 60) + '.tsv'

                upload_file(local_data_file_path, remote_data_file_path)
                # Bir dakikalık datası dolmuş olan local_data_file'ı, Bucket'a yüklüyoruz.
                active_file_time = new_file_time
                new_local_data_file_path = './data/' + str(int(active_file_time * 60)) + '.tsv'

                f = open(new_local_data_file_path, 'w')
                print(' #' * 50)
                print(' #' * 50)
                print(' #' * 50)
                print(' #' * 20 + ' new file:' + new_local_data_file_path + ' #' * 20)
                print(' #' * 50)
                print(' #' * 50)
                print(' #' * 50)

            timestamp = f"{datetime.datetime.fromtimestamp(int(res['T'] / 1000)):%Y-%m-%d %H:%M:%S}"
            maker = '0'
            if res['m']: # Satın almış ise 1, satış yaptı ise 0.
                maker = '1'


            line = str(res['t']) + '\t'
            line+= str(res['s']) + '\t'
            line+= '{:.2f}'.format(round(float(res['p']), 2)) + '\t'
            line+= str(res['q'])[0:-3] + '\t'
            line+= str(timestamp) + '\t'
            line+= str(maker) + '\n'
            f.write(line)
            # Line oluşturuldu
            print(line)
            # print(res)

    await client.close_connection()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
