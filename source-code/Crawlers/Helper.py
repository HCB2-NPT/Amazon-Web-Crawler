import requests
import time

class Helper:
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'x-wl-uid=1ufpx359OBHL3vTgz/MbR7JgvkGJQRhz3LckdkNugbfHLCGPk7vetOZISd2oWd2WSJfsVdg2IorQ=; aws-session-id=160-6219495-6698944; aws-session-id-time=2102609170l; aws-ubid-main=158-6490660-4063723; s_pers=%20s_vnum%3D1474481169449%2526vn%253D1%7C1474481169449%3B%20s_invisit%3Dtrue%7C1471890969449%3B; session-token="GFYnOfaa8viObgPPKTFbjsjtj/hdS0xHe8XNxHlZ6bDpw/7cg59WOVThx4zcoPrv5qYG69uqL0Excw9ips2zxkJ/BZsdEYRMnlblx4vGeno59jEosFKNgWwelK2xxDUCyus3M8Sk+kb5jnJVHFfeBrN6g1Flud/Dn0YCpygq7J3MZSdA1GGRGS9DsL45rMKGSpXeKVdF0ObGtEfhUMXYlg=="; skin=noskin; session-id-time=2082787201l; session-id=164-0077019-9402407; csm-hit=WQ4QTWMJ1572HGJK4CTE+s-WQ4QTWMJ1572HGJK4CTE|1474103087986; ubid-main=191-7802258-0837316'
    }

    @staticmethod
    def parseHMTL(link):
        try:
            html = requests.get(link, headers = Helper.headers)
        except Exception, e:
            time.sleep(1)
            html = requests.get(link, headers = Helper.headers)
        return html.content