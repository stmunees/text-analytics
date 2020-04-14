import os
import pandas as pd
import warnings


def generate_data(csvpath,percent=1,distrib=[50,50]):
  '''
  Generates Data according to the paramters and returns
  one dataframe with all data as per requirement.

  csvpath: give directory path to the entire csv file (~3.5GB). Its on GDrive.

  percent: Total entries = 5.26 Million, input the % of this, you want TOTALLY.
           Range = 0 to 100, type = int or float.
           Default = 1

  distrib: This asks for distribution of +ve and -ve reviews.
           positive (>4 stars) and negative (<2 stars) in a list.
           Range = 0 to 100, type = integer.
           Sample [40,60]. 40% is positive, 60% is negative.
           Default = [50,50]
  '''

  exception_handling(csvpath,percent=percent,distrib=distrib)
  print("Reading CSV....(Might take around 1:30mins to 2mins- 3.5GB file)")
  test = pd.read_csv(csvpath)
  print("Reading Done.")
  del test['review_id']
  del test['user_id']
  del test['business_id']
  del test['funny']
  del test['cool']
  star_count=[]
  for i in range(1,6):
    star_count.append(test[test['stars']==i].shape[0])
  total_pos_count = star_count[3]+star_count[4]
  total_neg_count = star_count[0]+star_count[1]
  num_data  = round((test.shape[0]*percent)/100)
  if(True):
    pos_req = round((num_data*distrib[0])/100)
    neg_req = round((num_data*distrib[1])/100)
    pos_test = test['stars']>=4
    neg_test = test['stars']<=2
    pos_test = test[pos_test]
    neg_test = test[neg_test]
    if (pos_req <= total_pos_count and neg_req <= total_neg_count):
      new_pos_df = pos_test.sample(pos_req)
      new_pos_df = new_pos_df.reset_index(drop=True)
      new_neg_df = neg_test.sample(neg_req)
      new_neg_df = new_neg_df.reset_index(drop=True)
      final_df=pd.concat([new_pos_df, new_neg_df], axis=0)
      index1=list(range(1,pos_req+1))
      index2=list(range(pos_req+1,final_df.shape[0]+1))
      index=index1+index2
      final_df.index=index
    else:
      if (pos_req <= total_pos_count and neg_req > total_neg_count):
        new_pos_df = pos_test.sample(pos_req)
        new_pos_df = new_pos_df.reset_index(drop=True)
        new_neg_df = neg_test.copy()
        new_neg_df = new_neg_df.reset_index(drop=True)
        final_df=pd.concat([new_pos_df, new_neg_df], axis=0)
        index1=list(range(1,pos_req+1))
        index2=list(range(pos_req+1,final_df.shape[0]+1))
        index=index1+index2
        final_df.index=index
        warnings.warn("\nUnable to satisfy negative reviews due to requirement"+
                      " being larger than availble in original CSV. \n"+
                      "Please modify percent and/or distrib accordingly. \n"+
                      "However used all negative reviews and generated, "+
                      "ratio may not be maintained.")
      if (pos_req > total_pos_count and neg_req <= total_neg_count):
        new_neg_df = neg_test.sample(neg_req)
        new_neg_df = new_neg_df.reset_index(drop=True)
        new_pos_df = pos_test.copy()
        new_pos_df = new_pos_df.reset_index(drop=True)
        final_df=pd.concat([new_neg_df, new_pos_df], axis=0)
        index1=list(range(1,neg_req+1))
        index2=list(range(neg_req+1,final_df.shape[0]+1))
        index=index1+index2
        final_df.index=index
        warnings.warn("\nUnable to satisfy positive reviews due to requirement"+
                      " being larger than availble in original CSV. \n"+
                      "Please modify percent and/or distrib accordingly. \n"+
                      "However used all positive reviews and generated, "+
                      "ratio may not be maintained.")
  print("Data Generated")
  return final_df


def exception_handling(csvpath,percent,distrib):
  '''
  Handles Exception for the function Generate Data
  '''
  if(type(percent)!=float and type(percent)!=int):
    raise TypeError('Percent should be int or float Value.')
  if(percent<0 or percent>100):
    raise ValueError('Percent Value should be between 0 and 100.')
  if(type(distrib)!=list):
    raise TypeError('Distribution parameter must be of list type.')
  if(len(distrib)!=2):
    raise IndexError('The Distribution list must be of length two')
  if(sum(distrib)!=100):
    raise ValueError('The sum of values of list distrib must be 100')
  if not(os.path.exists(csvpath)):
    raise FileNotFoundError('Please give a correct path to the entire Yelp'+
                            ' Review CSV.')

#Sample Code calling Function
#filepath='drive/My Drive/Text Analytics/Dataset/yelp_review.csv'
#data = generate_data(filepath,percent=10)
