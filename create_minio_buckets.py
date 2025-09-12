#!/usr/bin/env python3
"""
Create MinIO buckets for AI-AH agent training
Uses direct API calls to create buckets
"""

import requests
import json
from datetime import datetime

class MinIOBucketCreator:
    def __init__(self):
        self.minio_url = "http://localhost:9000"
        self.minio_console = "http://localhost:9001"
        self.access_key = "minioadmin"
        self.secret_key = "minioadmin123"
        
        # Buckets to create for agent training
        self.buckets = [
            "terraform-state",
            "ansible-artifacts", 
            "kubernetes-backups",
            "security-reports",
            "monitoring-data",
            "ai-training-data"
        ]

    def create_bucket(self, bucket_name):
        """Create a bucket using MinIO API"""
        try:
            # MinIO uses AWS S3-compatible API
            url = f"{self.minio_url}/{bucket_name}"
            
            # Create bucket with PUT request
            response = requests.put(
                url,
                auth=(self.access_key, self.secret_key),
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"  ✅ Created bucket: {bucket_name}")
                return True
            else:
                print(f"  ❌ Failed to create bucket {bucket_name}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error creating bucket {bucket_name}: {str(e)}")
            return False

    def list_buckets(self):
        """List existing buckets"""
        try:
            url = f"{self.minio_url}/"
            response = requests.get(
                url,
                auth=(self.access_key, self.secret_key),
                timeout=10
            )
            
            if response.status_code == 200:
                print("  📋 Existing buckets:")
                # Parse XML response (MinIO returns XML for bucket listing)
                content = response.text
                if "<Name>" in content:
                    import re
                    bucket_names = re.findall(r'<Name>(.*?)</Name>', content)
                    for bucket in bucket_names:
                        print(f"    - {bucket}")
                else:
                    print("    (No buckets found)")
                return True
            else:
                print(f"  ❌ Failed to list buckets: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error listing buckets: {str(e)}")
            return False

    def test_connection(self):
        """Test connection to MinIO"""
        try:
            # Test health endpoint
            health_url = f"{self.minio_url}/minio/health/live"
            response = requests.get(health_url, timeout=5)
            
            if response.status_code == 200:
                print("  ✅ MinIO connection successful")
                return True
            else:
                print(f"  ❌ MinIO health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"  ❌ MinIO connection failed: {str(e)}")
            return False

    def create_all_buckets(self):
        """Create all required buckets for agent training"""
        print("🗄️ Creating MinIO Buckets for Agent Training")
        print("=" * 50)
        
        # Test connection first
        if not self.test_connection():
            print("❌ Cannot connect to MinIO. Please check if MinIO is running.")
            return False
        
        # List existing buckets
        print("\n📋 Checking existing buckets...")
        self.list_buckets()
        
        # Create buckets
        print(f"\n🚀 Creating {len(self.buckets)} buckets...")
        created_count = 0
        
        for bucket in self.buckets:
            if self.create_bucket(bucket):
                created_count += 1
        
        # List buckets after creation
        print(f"\n📋 Buckets after creation:")
        self.list_buckets()
        
        print(f"\n📊 Summary:")
        print(f"  Total buckets to create: {len(self.buckets)}")
        print(f"  Successfully created: {created_count}")
        print(f"  Failed: {len(self.buckets) - created_count}")
        
        if created_count == len(self.buckets):
            print("  ✅ All buckets created successfully!")
            return True
        else:
            print("  ⚠️ Some buckets failed to create")
            return False

def main():
    """Main function"""
    creator = MinIOBucketCreator()
    success = creator.create_all_buckets()
    
    if success:
        print("\n🎉 MinIO buckets ready for agent training!")
        print("\n📋 Next steps:")
        print("  1. Test agents with real MinIO integration")
        print("  2. Validate bucket access from agents")
        print("  3. Test actual data storage and retrieval")
    else:
        print("\n❌ Bucket creation had issues. Check MinIO status.")

if __name__ == "__main__":
    main()
