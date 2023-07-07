# EC2, EBS, EKS, ES, RDS
# EC2 - auto scaling 무료
# ELB -> 전송한 네트워크 트래픽의 양 GB 를 가져올 수가 없음
# ECR -> ELB 랑 같은 이유
# S3 -> 있다고 해야 하나 ?
from config.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import boto3, json
from datetime import datetime, timedelta
from botocore.config import Config
my_config = Config(
    region_name = 'ap-south-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10
    }
)

auth = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

ec2 = auth.client('ec2')
eks = auth.client('eks')
es = auth.client('opensearch')
rds = auth.client('rds')
pricelist = auth.client('pricing', config=my_config)

def CostEC2():
    # 현재 사용하고 있는 EC2 instance ID & Type 조회 -> 단가 조회 (PriceList)
    all_ec2 = ec2.describe_instances()
    ec2_sum = 0
    for i in range(len(all_ec2['Reservations'])):
        instance_id = all_ec2['Reservations'][i]['Instances'][0]['InstanceId']
        instance_type = all_ec2['Reservations'][i]['Instances'][0]['InstanceType']

        # PriceList API : 가격 조회
        price_response = pricelist.get_products(
            ServiceCode='AmazonEC2',
            Filters=[
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'instanceType',
                    'Value': instance_type  # 원하는 인스턴스 유형으로 변경
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'location',
                    'Value': 'Asia Pacific (Seoul)'  # 원하는 지역으로 변경
                }
            ]
        )
        price_json = json.loads(price_response['PriceList'][0])
        if instance_type == 't2.medium':
            instance_price = price_json["terms"]["OnDemand"]['29JPFW5PYGJN2MX2.JRTCKXETXF']["priceDimensions"][
                '29JPFW5PYGJN2MX2.JRTCKXETXF.6YS6EN2CT7']["pricePerUnit"]["USD"]
        elif instance_type == 't3.medium':
            instance_price = price_json["terms"]["OnDemand"]['2AF3YZ9VV6EDYTEX.JRTCKXETXF']["priceDimensions"][
                '2AF3YZ9VV6EDYTEX.JRTCKXETXF.6YS6EN2CT7']["pricePerUnit"]["USD"]
        elif instance_type == 't3.xlarge':
            instance_price = price_json["terms"]["OnDemand"]['24GPMCAUP9P4GSC6.JRTCKXETXF']["priceDimensions"][
                '24GPMCAUP9P4GSC6.JRTCKXETXF.6YS6EN2CT7']["pricePerUnit"]["USD"]

        # 사용 시간 (1시간 단위)
        usage_time = 24

        # 가격 계산 : 시간 * 가격
        instance_price = float(instance_price) * usage_time
        ec2_sum += instance_price
        print("인스턴스 ID :", instance_id, ',', "인스턴스 Type :", instance_type, ',', "인스턴스 가격 : $", instance_price)
    print("EC2 총 가격 : $", ec2_sum)
    return ec2_sum

def CostEBS():
    all_ebs = ec2.describe_volumes()
    ebs_list = all_ebs['Volumes']
    ebs_sum = 0

    for i in range(len(ebs_list)):
        volume_id = ebs_list[i]['VolumeId']
        volume_type = ebs_list[i]['VolumeType']
        volume_size = ebs_list[i]['Size']

        # 범용 SSD(gp2) 볼륨 : 월별 프로비저닝된 스토리지 GB당 0.114 USD
        # gp2 볼륨용으로 프로비저닝된 스토리지는 초 단위로 청구
        # 24시간 = 86400초, 한 달 30일 기준
        # 월별 GB당 0.114 * volume_size(GB) * 하루에 돌아가는 시간(86400초) / (86400초/일 * 한 달 30일)) = 합계 : 한 달 30일 USD
        ebs_price = volume_size * 0.114 * 86400 / (86400 * 30)
        ebs_sum += ebs_price

        print("Volume Id :", volume_id, ', Volume Type :', volume_type, ', Volume Size(GB) :', volume_size,
              ', Volume Price : ', ebs_price)
    print("EBS 총 가격 : $", ebs_sum)


    # ebs 볼륩 스냅샷 스토리지
    snapshots = ec2.describe_snapshots(
        OwnerIds=['728156710202']
    )
    all_snaps = snapshots['Snapshots']
    snaps_sum = 0
    for j in range(len(all_snaps)):
        snaps_id = all_snaps[j]['SnapshotId']
        snaps_size = all_snaps[j]['VolumeSize']
        # EBS Snapshots 스토리지 요금 - 스탠더드 : 0.05 USD/월별 GB당
        snaps_price = snaps_size * 0.05 * 86400 / (86400 * 30)
        snaps_sum += snaps_price
        print("스냅샷 id :", snaps_id, ', 스냅샷 size :', snaps_size, ', 스냅샷 price : $', snaps_price)
    print("EBS Snapshots 총 가격 : $", snaps_sum)
    return ebs_sum + snaps_sum

def CostEKS():
    # 현재 사용하고 있는 EKS 조회
    all_eks = eks.list_clusters()
    cluster_list = all_eks['clusters']
    eks_sum = 0
    for i in range(len(cluster_list)):
        # 생성하는 각 Amazon EKS 클러스터에 대해 시간당 0.10 USD를 지불합니다
        # 가격 = 시간 * 클러스터 개수 * 단가
        usage_time = 24
        eks_price = usage_time * 1 * 0.10
        eks_sum += eks_price
        print("EKS 이름 :", cluster_list[i], ',', "EKS 가격 : $", eks_price)
    print("EKS 총 가격 : $", eks_sum)
    return eks_sum

def CostES():
    # 현재 사용하고 있는 ES 조회
    all_es = es.list_domain_names(EngineType='Elasticsearch')
    es_list = all_es['DomainNames']
    es_sum = 0  # 총 비용 계산 변수
    for i in range(len(es_list)):
        es_name = es_list[i]['DomainName']
        response = es.describe_domain(
            DomainName=es_name
        )
        es_instance_type = response['DomainStatus']['ClusterConfig']['InstanceType']
        es_nodes_num = response['DomainStatus']['ClusterConfig']['InstanceCount']
        # m5.large.search 시간당 0.174 USD
        # 가격 = 시간 * 단가 * 인스턴스 노드 개수
        usage_time = 24
        es_price = usage_time * 0.174 * es_nodes_num
        es_sum += es_price
        print("ES 이름 :", es_name, ',', "ES 인스턴스 타입 :", es_instance_type, ',', 'ES 노드 개수 :', es_nodes_num, ", ES 가격 : $",
              es_price)

    print("ES 총 가격 : $", es_sum)
    return es_sum



def CostRDS():
    # 현재 사용하고 있는 RDS name&type 조회
    all_rds = rds.describe_db_instances()
    rds_sum = 0
    for i in range(len(all_rds['DBInstances'])):
        rds_name = all_rds['DBInstances'][i]['DBInstanceIdentifier']
        rds_type = all_rds['DBInstances'][i]['DBInstanceClass']

        # PriceList API : 가격 조회
        price_response = pricelist.get_products(
            ServiceCode='AmazonRDS',
            Filters=[
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'instanceType',
                    'Value': rds_type  # 원하는 인스턴스 유형으로 변경
                },
                {
                    'Type': 'TERM_MATCH',
                    'Field': 'location',
                    'Value': 'Asia Pacific (Seoul)'  # 원하는 지역으로 변경
                }
            ]
        )

        price_json = json.loads(price_response['PriceList'][0])
        rds_price = price_json["terms"]["OnDemand"]["26GQ7SXFMG8Q4KN2.JRTCKXETXF"]["priceDimensions"][
            "26GQ7SXFMG8Q4KN2.JRTCKXETXF.6YS6EN2CT7"]["pricePerUnit"]["USD"]

        # 사용 시간 (1시간 단위)
        usage_time = 24

        # 가격 계산 : 시간 * 가격
        rds_price = float(rds_price) * usage_time
        rds_sum += rds_price
        print("RDS Name :", rds_name, ',', "RDS Type :", rds_type, ',', "RDS price : $", rds_price)

    print("RDS 총 가격 : $", rds_sum)

    return rds_sum

def CostS3():
    # S3 standard : 스토리지 요금 - 처음 50TB/월 - GB당 0.025 USD
    s3_sum = 0
    return s3_sum

day_of_usage = CostEC2() + CostEBS() + CostEKS() + CostES() + CostRDS()
print('하루 총 비용 : $', day_of_usage)
'''

# rds 저장할 때 - 오늘 날짜
print(datetime.today().strftime("%Y%m%d"))

# 어제 날짜 :
# yesterday = datetime.today() - timedelta(1)
# print(yesterday.strftime("%Y%m%d"))
'''