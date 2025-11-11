from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("loadDataAnalysis").getOrCreate()

df = spark.read.csv("file:///home/en_han/aws_powerflow_demo/household_data_1min_singleindex.csv", header=True, inferSchema=True)

df.show(5)  

spark.stop()