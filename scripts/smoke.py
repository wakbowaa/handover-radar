import json,re,time
from pathlib import Path
from genlayer_py import create_account,create_client
from genlayer_py.chains import studionet
from genlayer_py.contracts import actions as ca
ca.make_calldata_object=lambda method=None,args=None,kwargs=None:{**({"method":method} if method else {}),**({"args":args} if args else {}),**({"kwargs":kwargs} if kwargs else {})}
R=Path(__file__).parents[1];E=(R.parents[3]/"accounts.env").read_text();K=re.search(r'^ACCOUNT_6_GENLAYER_PRIVATE_KEY\s*=\s*"?([^"\r\n]+)',E,re.M).group(1).strip();c=create_client(chain=studionet,account=create_account(account_private_key=K));A=json.loads((R/"deployment.json").read_text())["contractAddress"]
def w(n,args):
 h=c.write_contract(address=A,function_name=n,args=args);print(n+"_tx="+str(h),flush=True);r=c.wait_for_transaction_receipt(transaction_hash=h,wait_until="finalized",retries=180,interval=5000,full_transaction=True);L=r.get("consensus_data",{}).get("leader_receipt") or [];L=[L] if isinstance(L,dict) else L;assert r.get("result_name")=="MAJORITY_AGREE" and any(x.get("execution_result")=="SUCCESS" for x in L);return str(h)
i="LIVE-WATCH-"+str(int(time.time()));topics=["Safety state","Open incidents","Next operator actions"];report="Safety state is normal with alarms tested at 06:00. Incident INC-42 remains open and is owned by Mira. The next operator must inspect pump B at 08:00 and record pressure before restart.";tx={"open":w("open_watch",[i,"North operations desk","Night to morning",json.dumps(topics),report]),"scan":w("scan",[i])};final=c.read_contract(address=A,function_name="get_watch",args=[i]);assert final["state"] in ("CLEARED","NEEDS_PATCH") and len(final["coverage"])==3;(R/"evidence"/"live-run.json").write_text(json.dumps({"id":i,"contract":A,"transactions":tx,"final":final},indent=2)+"\n");print(json.dumps(final,indent=2))

