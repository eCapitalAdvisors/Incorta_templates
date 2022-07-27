# Created By: Lila W Sahar
# Created Date: 07/15/2022
# version = '1.0'

# ---------------------------------------------------------------------------
""" This script is made to take a Materialized View and use it for a linear regression """ 
# ---------------------------------------------------------------------------

# Imports
from pyspark.sql.functions import mean
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit

# Data Load
data = read('Price_Elasticity.Data_Processed')

# Grouping
data = data.groupBy('ProductID', 'ProductName') \
    .agg(mean('UnitPrice').alias('AvgPrice'), mean('StandardCost').alias('AvgCost'))

# Transformation
assembler = VectorAssembler(inputCols = ['AvgPrice'], outputCol = 'Features')

output = assembler.transform(data)
output.select('Features')
finalized_data = output.select('Features', 'AvgCost')

# Train-Test
train, test = finalized_data.randomSplit([0.75, 0.25])

# Model
lr = LinearRegression()\
    .setParams(featuresCol = 'Features', labelCol = 'AvgCost')

# Model Fitting
lr = lr.fit(train)

# Export
pred_results = lr.evaluate(test)

result = pred_results.predictions
save(result)


## perfect the output
# output = prediction.drop("unscaledFeatures", "features").withColumnRenamed("prediction", "Cluster")