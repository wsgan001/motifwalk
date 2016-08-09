import graph as g
import embeddings as e
import pickle as p

bc = g.graph_from_pickle('../data/blogcatalog3.graph')
model=e.EmbeddingNet(graph=bc)
model.build()
model.train(num_nodes_per_batch=200)
weights = model.get_weights()
with open('random_bs400_ns10.weights', 'wb') as f:
    p.dump(weights, f, p.HIGHEST_PROTOCOL)
