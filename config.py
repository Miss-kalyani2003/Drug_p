import os
import pymongo
MONGO_URL="mongodb://localhost:27017"
MONGO_DB_NAME="drug_db_new"
MODEL_FILE_PATH=os.path.join("artifact","logisticRegression.pkl")
LABEL_ENCODED_DATA=os.path.join("artifact",'label_encoding.json')