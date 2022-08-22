from binance import AsyncClient, BinanceSocketManager
import asyncio
import time
import datetime
import os

async def main():

    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    trade_socket = bm.trade_socket('BTCUSDT')
    # BTCUSDT parametresindeki market hareketlerinin datasını istiyoruz.
    async with trade_socket as tscm:
        while True:
            res = await tscm.recv()
            print(res)

            new_file_time = int(res['T'] / (1000 * 60))
            # Gelen datanın içindeki unixtime'ı (milisecond cinsinden) dakikaya çeviriyoruz.




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

            # Line oluşturuldu
            print(line)
            # print(res)

    await client.close_connection()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())