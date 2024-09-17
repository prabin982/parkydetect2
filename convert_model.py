from pyexpat import model
import xgboost as xgb

# Assuming 'model' is your trained XGBoost model
model.save_model('C:\labedc\ParkinSeen-master\static')
import xgboost as xgb

# Load the model in the current XGBoost version
model = xgb.Booster(model_file='C:\labedc\ParkinSeen-master\static')

