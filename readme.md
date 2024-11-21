# Kafka Producer-Consumer with Prometheus Monitoring

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup and Running](#setup-and-running)
- [Services Description](#services-description)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [License](#license)

## Overview

This project sets up a Kafka-based producer and consumer system monitored by Prometheus and visualized with Grafana. The setup is containerized using Docker Compose, ensuring easy deployment and scalability. The producer and consumer are Python applications that send and receive messages to and from a Kafka topic, respectively, while collecting metrics for monitoring purposes.

## Architecture

The system consists of the following components:

- **Kafka Broker (`kafka_b`)**: Manages message storage and distribution.
- **Init Topics (`init-topics`)**: Initializes Kafka topics.
- **Producer (`producer`)**: Sends messages to Kafka.
- **Consumer (`consumer`)**: Consumes messages from Kafka.
- **Prometheus (`prometheus`)**: Collects and stores metrics.
- **Grafana (`grafana`)**: Visualizes metrics from Prometheus.

![Architecture Diagram](architecture.png) *(Include an architecture diagram if available)*

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Setup and Running

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Ensure Docker is Running**

   Make sure Docker is installed and the Docker daemon is running on your machine.

3. **Build and Start the Services**

   Run the following command to build the Docker images and start all services:

   ```bash
   docker-compose up --build
   ```

   This command will:

   - Build the producer and consumer Docker images.
   - Start the Kafka broker, initialize the Kafka topic, and run the producer and consumer scripts.
   - Launch Prometheus and Grafana for monitoring.

4. **Access the Services**

   - **Prometheus**: [http://localhost:9090](http://localhost:9090)
   - **Grafana**: [http://localhost:3000](http://localhost:3000)  
     - **Default Credentials**:  
       - **Username**: `admin`  
       - **Password**: `admin`
   - **Producer Metrics**: [http://localhost:8000](http://localhost:8000)
   - **Consumer Metrics**: [http://localhost:8001](http://localhost:8001)

## Services Description

### 1. Kafka Broker (`kafka_b`)

- **Image**: `bitnami/kafka:latest`
- **Ports**:
  - `9092`: PLAINTEXT for host access
  - `9093`: CONTROLLER listener
- **Environment Variables**:
  - Configurations for Kafka listeners, advertised listeners, broker ID, etc.
- **Healthcheck**: Ensures Kafka is ready before other services start.

### 2. Init Topics (`init-topics`)

- **Image**: `bitnami/kafka:latest`
- **Command**: Creates the `test-topic` with 3 partitions and replication factor of 1.
- **Depends On**: Waits for Kafka broker to be healthy.

### 3. Producer (`producer`)

- **Image**: `python:3.9-slim`
- **Ports**:
  - `8000`: Exposes Prometheus metrics
- **Command**:
  - Installs dependencies and runs `producer.py`
- **Functionality**:
  - Sends 10 messages to `test-topic` and exposes metrics.

### 4. Consumer (`consumer`)

- **Image**: `python:3.9-slim`
- **Ports**:
  - `8001`: Exposes Prometheus metrics
- **Command**:
  - Installs dependencies and runs `consumer.py`
- **Functionality**:
  - Consumes 10 messages from `test-topic` and exposes metrics.

### 5. Prometheus (`prometheus`)

- **Image**: `prom/prometheus:latest`
- **Ports**:
  - `9090`: Prometheus UI
- **Configuration**:
  - Uses `prometheus.yml` for scraping metrics from producer and consumer.

### 6. Grafana (`grafana`)

- **Image**: `grafana/grafana:latest`
- **Ports**:
  - `3000`: Grafana UI
- **Environment Variables**:
  - Sets default admin username and password.

## Monitoring

### Prometheus

Prometheus is configured to scrape metrics from the producer and consumer applications running on ports `8000` and `8001` respectively. You can access the Prometheus UI at [http://localhost:9090](http://localhost:9090) to query and visualize metrics.

### Grafana

Grafana is set up to visualize metrics collected by Prometheus. Access Grafana at [http://localhost:3000](http://localhost:3000) using the default credentials (`admin` / `admin`). You can import or create dashboards to monitor Kafka producer and consumer metrics.

## Troubleshooting

### Issue: `NoBrokersAvailable: NoBrokersAvailable`

**Symptom**: Producer and consumer services cannot connect to Kafka broker, resulting in `NoBrokersAvailable` error.

**Cause**: The producer and consumer were initially configured to connect to `localhost:9092`. Within Docker containers, `localhost` refers to the container itself, not the Kafka broker container.

**Solution**:

1. **Update `bootstrap_servers`**: Ensure that in both `producer.py` and `consumer.py`, the `bootstrap_servers` parameter is set to `kafka_b:9092` instead of `localhost:9092`.

   ```python
   # producer.py
   producer = KafkaProducer(bootstrap_servers='kafka_b:9092')
   
   # consumer.py
   consumer = KafkaConsumer(
       'test-topic',
       bootstrap_servers='kafka_b:9092',
       ...
   )
   ```

2. **Rebuild and Restart Containers**:

   ```bash
   docker-compose down
   docker-compose up --build
   ```

### Other Common Issues

- **Ports Already in Use**: Ensure that the required ports (`9092`, `9093`, `8000`, `8001`, `9090`, `3000`) are not occupied by other services on your host machine.
  
- **Kafka Not Starting**: Check Kafka broker logs for any errors. Ensure that environment variables are correctly set in `docker-compose.yml`.

- **Metrics Not Visible**: Verify that Prometheus is correctly scraping metrics from producer and consumer by checking Prometheus targets at [http://localhost:9090/targets](http://localhost:9090/targets).

## Best Practices

- **Use Environment Variables**: Manage configurations using environment variables to make your setup more flexible and secure.

- **Implement Retry Logic**: Incorporate retry mechanisms in your producer and consumer scripts to handle transient connection issues.

- **Use Virtual Environments**: Avoid running `pip` as the `root` user to prevent permission issues. Use Python virtual environments to manage dependencies.

- **Keep Dependencies Updated**: Regularly update `pip` and Python packages to benefit from the latest features and security patches.

## License

This project is licensed under the [MIT License](LICENSE).

---

*Feel free to contribute to this project by opening issues or submitting pull requests.*