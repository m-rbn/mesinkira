import sys
import logging

from awsglue.job import Job
from awsglue.context import GlueContext
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.context import SparkContext
from awsglue.utils import getResolvedOptions

input_path = "s3://my-bucket/input/data.csv"
output_path = "s3://my-bucket/output/filtered_data/"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# I'm using col_a and col_b as placeholder for the other columns names as example
csv_schema = StructType([
    StructField('col_a', StringType(), True),
    StructField('col_b', StringType(), True),
    StructField('sentiment_score', DoubleType(), True)
])

def read_input(spark_session, input_s3_path, schema):
    logger.info('Start reading file..')
    df = (
        spark_session
          .read.option('header', 'true')
          .schema(schema)
          .csv(input_s3_path)
    )

    return df

def filter_score(df, col_to_filter, max_score):
    filtered_df = df.filter(df[col_to_filter] < max_score)
    logger.info(f"Filtered data down to {filtered_df.count()} rows where {col_to_filter} < 0.5")

    return filtered_df

# Writes output to new .csv file
def write_output(filtered_df, output_s3_path):
    filtered_df.write.option("header", "true").mode("overwrite").csv(output_s3_path)
    logger.info(f"Successfully wrote filtered data to: {output_s3_path}")

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
job.init(args['JOB_NAME'], args)

df = read_input(spark, input_path, csv_schema)
filtered_df = filter_score(df, 'sentiment_score', 0.5)
write_output(filtered_df, output_path)

job.commit()