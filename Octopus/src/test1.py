import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"
from pyspark.sql import SparkSession

# 打印 Java 主目录（可选，用于调试）
print("JAVA_HOME:", os.environ.get('JAVA_HOME', 'Not set'))

# 尝试创建最简单的 SparkSession
spark = SparkSession.builder \
    .appName("Java17Test") \
    .master("local[*]") \
    .getOrCreate()

print(f"✅ Spark 成功启动！版本：{spark.version}")
print(f"✅ Spark 使用的 Java 版本：{spark._jvm.java.lang.System.getProperty('java.version')}")

# 创建一个简单的 DataFrame 并显示
df = spark.createDataFrame([(1, "Alice"), (2, "Bob")], ["id", "name"])
df.show()

spark.stop()