from ipaddress import (
    IPv4Network,
    IPv6Network,
)

ADMIN_PORTS = {
    22,  # SSH
    1521,  # Oracle
    1433,  # MSSQL
    1434,  # MSSQL
    2438,  # Oracle
    3306,  # MySQL
    3389,  # RDP
    5432,  # Postgres
    6379,  # Redis
    7199,  # Cassandra
    8111,  # DAX
    8888,  # Cassandra
    9160,  # Cassandra
    11211,  # Memcached
    27017,  # MongoDB
    445,  # CIFS
}

UNRESTRICTED_IPV4 = IPv4Network("0.0.0.0/0")
UNRESTRICTED_IPV6 = IPv6Network("::/0")
