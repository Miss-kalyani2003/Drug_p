import config
import json
import pickle
import numpy as np
import pandas as pd

class Drug():

    def __int__(self):
        pass

    def load_model(self):
        with open(config.MODEL_FILE_PATH,'rb') as f:
            self.model=pickle.load(f)
        return self.model
    
    def json_data(self):
        with open(config.LABEL_ENCODED_DATA,'r') as f:
            self.json_model=json.load(f)
        return self.json_model
    
    def create_test_array(self):
        self.load_model()
        self.json_data()

        test_array=np.zeros(( 1,self.model.n_features_in_))
        test_array[0,0]=self.data['Age']
        test_array[0,1]=self.json_model['Sex'][self.data['Sex']]
        test_array[0,2]=self.json_model['BP'][self.data['BP']]
        test_array[0,3]=self.json_model['Cholesterol'][self.data['Cholesterol']]
        test_array[0,4]=self.data['Na_to_K']

        self.test_df=pd.DataFrame(test_array,columns=self.model.feature_names_in_)

    def predict_Drug(self,user_data_input):
        self.data=user_data_input
        self.create_test_array()
        

        pred=self.model.predict(self.test_df)[0]
        print(pred)
        return pred

        

    

