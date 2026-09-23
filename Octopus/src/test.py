import os
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
import pandas as pd

# 可选：显式设置 JAVA_HOME（如果未来运行其他脚本有问题可取消注释）
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

print("步骤1: 配置 SparkSession 并启用 Delta Lake 扩展...")
builder = SparkSession.builder \
    .appName("CreateDeltaFileOnWSL") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

print(f"✅ Spark {spark.version} 已启动，使用 Java {spark._jvm.java.lang.System.getProperty('java.version')}")

# 创建与之前完全相同的示例数据
print("\n步骤2: 创建示例数据...")
people_df = pd.DataFrame([
    {"name": "Lai Hui", "address": "805 John Oval Apt. 470\nLake Amanda, NE 09043",
     "phone_number": "3087607759", "user_id": "16b74cfe-d9da-11ea-8534-0242ac110002", "device_id": 1},
    {"name": "Armando Clemente", "address": "293 Keith Drive\nEast David, NY 05983",
     "phone_number": "8497224309", "user_id": "16b78264-d9da-11ea-8534-0242ac110002", "device_id": 2},
    {"name": "Meallan O'Conarain", "address": "3048 Guerrero Alley\nJerryhaven, PA 56888",
     "phone_number": "(580)703-9076x32254", "user_id": "16b79f9c-d9da-11ea-8534-0242ac110002", "device_id": 3},
])

people_spark_df = spark.createDataFrame(people_df)
print("示例数据 schema:")
people_spark_df.printSchema()

# 写入 Delta 格式
print("\n步骤3: 写入 Delta Lake 格式...")
output_path = "/mnt/c/Users/210838672/Documents/GitHub/Octopus/src"  # Linux 原生路径
people_spark_df.write.format("delta").mode("overwrite").save(output_path)

print(f"✅ Delta 文件已成功生成在: {output_path}")

# 验证步骤
print("\n" + "="*50)
print("验证步骤")
print("="*50)

# 验证1：读取并显示数据
print("\n验证1: 读取 Delta 表并显示内容")
df_read = spark.read.format("delta").load(output_path)
df_read.show()

# 验证2：查看生成的文件结构
print("\n验证2: 文件结构 (通过 dbutils.fs.ls 模拟)")
# 注意: 在非Databricks环境中，我们使用 os 和 subprocess 来查看
import subprocess
try:
    print(f"目录内容:")
    subprocess.run(["ls", "-la", output_path], check=True)
    print(f"\n事务日志 (_delta_log) 内容:")
    subprocess.run(["ls", "-la", f"{output_path}/_delta_log"], check=True)
except Exception as e:
    print(f"无法列出文件详情，但 Delta 表已创建。错误: {e}")

# 验证3：使用 Delta 的时间旅行功能 (核心特性)
print("\n验证3: 测试 Delta 时间旅行 (查询版本 0)")
df_version0 = spark.read.format("delta").option("versionAsOf", 0).load(output_path)
print(f"版本 0 的记录数: {df_version0.count()}")

# 验证4：查看表历史
print("\n验证4: 查看 Delta 表历史")
from delta.tables import DeltaTable
delta_table = DeltaTable.forPath(spark, output_path)
history_df = delta_table.history()
history_df.select("version", "timestamp", "operation", "operationParameters").show(truncate=False)

# 验证5：执行更新操作展示 ACID 事务
print("\n验证5: 执行更新操作 (将 device_id = 1 的名字更新)")
delta_table.update("device_id = 1", {"name": "'Lai Hui (Updated)'"})

print("更新后的数据:")
delta_table.toDF().show()

print("\n验证6: 查看更新后的历史")
history_df_after = delta_table.history()
history_df_after.select("version", "timestamp", "operation", "operationParameters").show(truncate=False)

spark.stop()
print("\n" + "="*50)
print("✅ 所有步骤完成！你已成功在 WSL 中创建并验证了 Delta Lake 表。")
print(f"Delta 表位置: {output_path}")
print("="*50)