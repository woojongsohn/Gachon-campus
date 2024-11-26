from flask import Flask, render_template, request, send_file
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

app = Flask(__name__)

# 방향성 그래프 생성
G = nx.DiGraph()

# 가중치가 있는 모든 엣지 추가
edges_with_weights = [
    ('A', 'B', 2), ('A', 'D', 2), ('A', 'I', 5), ('A', 'O', 6), ('A', 'H', 5), ('A', 'R', 12),
    ('B', 'A', 2), ('B', 'C', 2), ('B', 'D', 3),
    ('C', 'B', 2), ('C', 'D', 2), ('C', 'E', 2), ('C', 'F', 6),
    ('D', 'A', 2), ('D', 'C', 2), ('D', 'E', 2), ('D', 'B', 3),
    ('E', 'C', 2), ('E', 'D', 2), ('E', 'F', 2), ('E', 'I', 8), ('E', 'G', 2),
    ('F', 'C', 2), ('F', 'E', 6), ('F', 'G', 0),
    ('G', 'F', 0), ('G', 'H', 4), ('G', 'J', 6),  ('G', 'E', 2),
    ('H', 'A', 10), ('H', 'D', 8), ('H', 'E', 6), ('H', 'G', 4), ('H', 'I', 8), ('H', 'J', 4), ('H', 'K', 4),
    ('I', 'A', 4), ('I', 'E', 12), ('I', 'L', 5), ('I', 'O', 7),
    ('J', 'G', 5), ('J', 'H', 3), ('J', 'I', 7),  ('J', 'K', 3), ('J', 'L', 2),
    ('K', 'H', 4), ('K', 'J', 3), ('K', 'L', 2),
    ('L', 'I', 8), ('L', 'J', 3), ('L', 'K', 3), ('L', 'P', 4),
    ('O', 'A', 5), ('O', 'P', 5), ('O', 'Q', 5),
    ('P', 'L', 4), ('P', 'O', 5), ('P', 'Q', 3),
    ('Q', 'O', 6), ('Q', 'P', 2), ('Q', 'R', 9),
    ('R', 'A', 8), ('R', 'Q', 8), ('R', 'S', 6),
    ('S', 'R', 7), ('S', 'T', 5), 
    ('T', 'S', 4), ('T', 'U', 8), ('T', 'V', 11),
    ('U', 'T', 8), ('U', 'V', 2),
    ('V', 'T', 12), ('V', 'U', 2)
]
G.add_weighted_edges_from(edges_with_weights)

# 노드의 고정 위치 설정 (지도 좌표계에 맞게 설정)
pos = {
    'A': (790, 370), 'B': (890, 250), 'C': (795, 165), 'D': (720, 225), 'E': (660, 170),
    'F': (700, 80),  'G': (600, 90),  'H': (430, 60),  'I': (585, 215), 'J': (390, 190),
    'K': (270, 260), 'L': (410, 330), 'O': (530, 430),
    'P': (310, 460), 'Q': (430, 570), 'R': (770, 560), 'S': (770, 650), 'T': (600, 720),
    'U': (210, 685), 'V': (270, 620)
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        source = request.form['source'].upper()
        target = request.form['target'].upper()


        try:
            # 다익스트라 알고리즘
            shortest_path = nx.dijkstra_path(G, source, target)
            shortest_distance = nx.dijkstra_path_length(G, source, target)

            # 경로 시각화
            path_edges = list(zip(shortest_path, shortest_path[1:]))
            img = Image.open("static/campus_map.png")  # 지도 이미지
            plt.figure(figsize=(12, 8))
            plt.imshow(img, extent=[0, 1000, 0, 800])
            nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=500, edge_color='gray', arrowsize=20, node_shape='o', linewidths=2, edgecolors='black')
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=3)
            
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
            
            plt.title(f"Shortest Path from {source} to {target}")
            plt.axis("off")
            plt.savefig('static/shortest_path.png')  # 결과 저장
            plt.close()


            return render_template('index.html', shortest_path=shortest_path, shortest_distance=shortest_distance, image='static/shortest_path.png')

        except nx.NetworkXNoPath:
            return render_template('index.html', error=f"{source}에서 {target}로 가는 경로가 없습니다.")
        except KeyError:
            return render_template('index.html', error="올바르지 않은 노드를 입력하셨습니다.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)