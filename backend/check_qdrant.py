"""
Quick script to check Qdrant collection status
"""
import sys
sys.path.append('src')

from src.services.vector_store import VectorStore

def check_qdrant_status():
    print("Connecting to Qdrant...")
    client = VectorStore.get_client()
    collection_name = VectorStore.get_collection_name()
    
    print(f"\nCollection name: {collection_name}")
    
    # Get collection info
    try:
        collection_info = client.get_collection(collection_name)
        print(f"\n✅ Collection exists!")
        print(f"Vector count: {collection_info.points_count}")
        print(f"Vector size: {collection_info.config.params.vectors.size}")
        
        if collection_info.points_count == 0:
            print("\n⚠️  WARNING: Collection is EMPTY! No data has been ingested.")
            print("Run the ingest script to populate the collection with book content.")
        else:
            print(f"\n✅ Collection has {collection_info.points_count} vectors!")
            
            # Try to get a sample point
            sample = client.scroll(
                collection_name=collection_name,
                limit=1
            )
            if sample[0]:
                print("\nSample document:")
                point = sample[0][0]
                print(f"  Source: {point.payload.get('source_file', 'N/A')}")
                print(f"  Content preview: {point.payload.get('content', '')[:100]}...")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    check_qdrant_status()
