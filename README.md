# orchestrators-benchmark
Orchestrators benchmark - Thesis project 


curl -X POST http://localhost:5000/api/assignments \
-H "Content-Type: application/json" \
-d '{
    "course_id": "TEST101",
    "title": "Primo Test dalla VM",
    "deadline": "2025-12-31T23:59:59Z",
    "max_file_size": 10
}'