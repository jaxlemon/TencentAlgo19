import math
import os
import numpy as np
import pandas as pd
import sys

def eval(submission_file,real_label_file,test_file):
        test_data = pd.read_csv(test_file, sep='\t',names=['index1','aid','create_timestamp','ad_size','ad_type_id','good_type','good_id','advertiser','delivery_periods','crowd_direction','bid']).sort_values(by='index1')
        real_label = pd.read_csv(real_label_file, sep='\t',names=['index2','real_label','gold']).sort_values(by='index2')

        #predict_label = pd.read_csv(submission_file,sep='\t',names=['index3','predict_label','gold']).sort_values(by='index3')
        predict_label = pd.read_csv(submission_file,sep='\t',names=['index3','predict_label']).sort_values(by='index3')
        predict_label = predict_label[['index3','predict_label']]
        test_data = pd.merge(test_data,real_label, left_index = True, right_index = True)

        test_data = pd.merge(test_data,predict_label,left_index = True, right_index = True)
        smape_data = test_data[test_data['gold'] == 1]
        score=abs(smape_data['real_label']-smape_data['predict_label'])/((smape_data['real_label']+smape_data['predict_label'])/2+1e-15)
        SMAPE=score.mean()
        best_score = 0
        try:
            last_aid=None
            gold_imp=None
            gold_bid=None
            s=None
            score=[]
            for item in test_data[['aid','bid','predict_label']].values:
                item=list(item)
                if item[0]!=last_aid:
                    last_aid=item[0]
                    gold_bid=item[1]
                    gold_imp=item[2]
                    if s is not None:
                        score.append(s/cont)
                    s=0
                    cont=0
                else:
                    if (gold_imp-item[2])*(gold_bid-item[1])==0:
                        s+=-1
                    else:
                        s+=((gold_imp-item[2])*(gold_bid-item[1]))/(abs(((gold_imp-item[2])*(gold_bid-item[1]))))
                    cont+=1

            MonoScore=np.mean(score)        
            score=0.8*(1-SMAPE/2)+0.2*(MonoScore+1)/2
        except:
            MonoScore=0

        if SMAPE<best_score:
            best_score=SMAPE
        print(("#AVG %.4f. Eval SMAPE %.4f. #Eval MonoScore %.4f. Best Score %.4f")%(test_data['predict_label'].mean(),SMAPE,MonoScore,best_score))
        return score
        

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Please provide the submission file when you run the script!")
    else:
        score = eval(sys.argv[1],"test_df_label.csv","test_df.csv")
        print(("#Your score is %.4f")%(score*100.0))
