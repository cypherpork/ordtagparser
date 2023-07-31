import asyncio
from noda import BTCnoda as Noda
from massage import MassageData as MassageData

fromnoda = Noda()
DataTLC = MassageData()

async def main():
    in_trxid = '12fb3283e8e9a4623edea5ba7a2f4209c173884ba595037a8365d74884715567'
    v_is_tag1_present, adjusted_outp_no, tags = await fromnoda.getTxTags(in_trxid,1 , True)
    tagarr = DataTLC.shapeTagArray(tags)
    print('v_is_tag1_present=', v_is_tag1_present, 'adjusted_outp_no=', adjusted_outp_no, 'tags=', tags)
    print(tagarr)
    for i in range(0, len(tagarr)):
        print(tagarr[i][0], tagarr[i][1], DataTLC.guessTag(tagarr[i][0], tagarr[i][1]))

if __name__ == "__main__":
    asyncio.run(main())
