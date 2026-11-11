"""KYC risk triage on synthetic data with synthetic review outcome labels."""
from projects.kyc import sample_customers,score_customers
LABELS={"SYN-001":0,"SYN-002":1,"SYN-003":0,"SYN-004":1,"SYN-005":0,"SYN-006":0}
def evaluate():
    records=score_customers(sample_customers())
    records["human_review_needed"]=records.customer_id.map(LABELS).astype(int)
    records["predicted"]=records.tier.eq("Priority").astype(int)
    tp=int(((records.predicted==1)&(records.human_review_needed==1)).sum())
    fp=int(((records.predicted==1)&(records.human_review_needed==0)).sum())
    fn=int(((records.predicted==0)&(records.human_review_needed==1)).sum())
    tn=len(records)-tp-fp-fn
    return {"confusion_matrix":{"TP":tp,"FP":fp,"FN":fn,"TN":tn},
            "precision":tp/(tp+fp) if tp+fp else 0,
            "recall":tp/(tp+fn) if tp+fn else 0,
            "review_queue":records}
if __name__=="__main__":
    print("ALL RECORDS & LABELS SYNTHETIC: no AML finding",evaluate())
