from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # تاکہ فرنٹ اینڈ سے ڈیٹا آسانی سے آ سکے

# تمام نوڈز کا ڈیٹا محفوظ کرنے کے لیے ڈکشنری
nodes_database = {}


@app.route("/")
def home():
  # کل پوائنٹس کا حساب لگانا
  total_points = sum(node["points"] for node in nodes_database.values())
  return jsonify({
      "status": "SleepEarn Server is Running 24/7",
      "total_active_nodes": len(nodes_database),
      "total_network_points": total_points,
      "nodes": nodes_database,
  })


@app.route("/sync", methods=["POST"])
def sync_node():
  data = request.json
  node_id = data.get("node_id")
  points = data.get("points", 0)
  seconds = data.get("seconds", 0)
  status = data.get("status", "Offline")

  if not node_id:
    return jsonify({"error": "Node ID is required"}), 400

  # نوڈ کا ڈیٹا اپ ڈیٹ یا محفوظ کریں
  nodes_database[node_id] = {
      "points": points,
      "seconds": seconds,
      "status": status,
  }

  return jsonify({
      "success": True,
      "message": f"Node {node_id} synced successfully",
      "current_node_data": nodes_database[node_id],
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
  
