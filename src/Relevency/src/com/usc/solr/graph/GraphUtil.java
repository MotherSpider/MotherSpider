package com.usc.solr.graph;

import java.awt.Dimension;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.StringTokenizer;

import javax.swing.JFrame;

import edu.uci.ics.jung.algorithms.layout.CircleLayout;
import edu.uci.ics.jung.algorithms.layout.Layout;
import edu.uci.ics.jung.algorithms.scoring.PageRank;
import edu.uci.ics.jung.graph.DirectedSparseGraph;
import edu.uci.ics.jung.visualization.BasicVisualizationServer;
import edu.uci.ics.jung.visualization.decorators.ToStringLabeller;
import edu.uci.ics.jung.visualization.renderers.Renderer.VertexLabel.Position;

public class GraphUtil {
	/**
	 * method to load grah data from a file and construct a graph
	 * @param in
	 * @param graph
	 * @throws IOException
	 */
	private void load_data (BufferedReader in, DirectedSparseGraph<String, Integer> graph) throws IOException {
		
		int edgeCnt = 0;
		String line;
		while ((line = in.readLine()) != null) {
		
			StringTokenizer st = new StringTokenizer(line);
			String source = null;
			if ( st.hasMoreTokens() ) {
				source = st.nextToken();
				if (graph.addVertex(source))
					System.out.println("Added vertex "+source+" to the graph");
			}

			HashSet<String> seen = new HashSet<String>() ;
			while ( st.hasMoreTokens() ) {
				String destination = st.nextToken();
				if (graph.addVertex(destination)) // implicit dangling nodes
					System.out.println("Added vertex "+destination+" to the graph");				
				if (!destination.equals(source)) { // no self-references
					if (!seen.contains(destination)) { // no duplicate links
						graph.addEdge(new Integer(edgeCnt++), source, destination);
						graph.addEdge(new Integer(edgeCnt++), destination, source);
						seen.add(destination) ;
					}
				}
			}
		}
		in.close();
		
	}
	/**
	 * method to add edge between matching features
	 * @param graph
	 * @param seen
	 * @param edgeCnt
	 * @param line
	 */
	public void addToGraph(DirectedSparseGraph graph,HashSet<String> seen,int edgeCnt,String line)
	{ 
		StringTokenizer st = new StringTokenizer(line);
		String source = null;
		if ( st.hasMoreTokens() ) {
			source = st.nextToken().trim();
			
			if (graph.addVertex(source))
				System.out.println("Added vertex "+source+" to the graph");
		}
		
		while ( st.hasMoreTokens() ) {
			String destination = st.nextToken().trim();
			if (graph.addVertex(destination)) // implicit dangling nodes
				System.out.println("Added vertex "+destination+" to the graph");				
			if (!destination.equals(source)) { // no self-references
				if (!seen.contains(destination)) { // no duplicate links
					graph.addEdge(new Integer(edgeCnt++), source, destination);
					graph.addEdge(new Integer(edgeCnt), destination, source);
				
					seen.add(destination) ;
				}
			}
		}
	}
	/**
	 * method to put edge for inlinks
	 * @param graph
	 * @param seen
	 * @param edgeCnt
	 * @param line
	 */
	public void addToGraph2(DirectedSparseGraph graph,HashSet<String> seen,int edgeCnt,String line)
	{ 
	        String source=line.split(" ")[0].trim();
			if (graph.addVertex(source))
				System.out.println("Added vertex "+source+" to the graph");
		
		
		
			String destination = line.split(" ")[1].trim();
			if (graph.addVertex(destination)) // implicit dangling nodes
				System.out.println("Added vertex "+destination+" to the graph");				
			if (!destination.equals(source)) { // no self-references
				if (!seen.contains(destination)) { // no duplicate links
					
					graph.addEdge(new Integer(edgeCnt++), destination, source);
				
					seen.add(destination) ;
				}
			}
		
	}
	/**
	 * method to construct edges for outlinks
	 * @param graph
	 * @param seen
	 * @param edgeCnt
	 * @param line
	 */
	public void addToGraph3(DirectedSparseGraph graph,HashSet<String> seen,int edgeCnt,String line)
	{ 
	        String source=line.split(" ")[0].trim();
			if (graph.addVertex(source))
				System.out.println("Added vertex "+source+" to the graph");
		
		
		
			String destination = line.split(" ")[1].trim();
			if (graph.addVertex(destination)) // implicit dangling nodes
				System.out.println("Added vertex "+destination+" to the graph");				
			if (!destination.equals(source)) { // no self-references
				if (!seen.contains(destination)) { // no duplicate links
					
					graph.addEdge(new Integer(edgeCnt++),source,destination);
				
					seen.add(destination) ;
				}
			}
		
	}
	
	
	
	public void displayGraph(DirectedSparseGraph graph)
	{
		//We create our graph in here
		 
		 Layout<Integer, String> layout = new CircleLayout(graph);
		 layout.setSize(new Dimension(400,400)); // sets the initial size of the space
		 // The BasicVisualizationServer<V,E> is parameterized by the edge types
		 BasicVisualizationServer<Integer,String> vv =
		 new BasicVisualizationServer<Integer,String>(layout);
		 vv.setPreferredSize(new Dimension(450,450)); //Sets the viewing area size
		 vv.getRenderContext().setVertexLabelTransformer(new ToStringLabeller());
		 vv.getRenderContext().setEdgeLabelTransformer(new ToStringLabeller());
		 vv.getRenderer().getVertexLabelRenderer().setPosition(Position.CNTR);

		 JFrame frame = new JFrame("Simple Graph View");
		 frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		 frame.getContentPane().add(vv);
		 frame.pack();
		 frame.setVisible(true); 
	}
	
	public static void main(String args[])
	{   GraphUtil myGraphOp= new GraphUtil();
		DirectedSparseGraph<String, Integer> graph = new DirectedSparseGraph<String, Integer>();
		
		try {
			BufferedReader data = new BufferedReader(new InputStreamReader(new FileInputStream("data/final_aoncadis_selenium_graph")));
			myGraphOp.load_data(data, graph);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		myGraphOp.displayGraph(graph);
		
		PageRank<String, Integer> ranker = new PageRank<String, Integer>(graph, 0.15);
		ranker.evaluate();
		//Map<Node, Double> result = new HashMap<Node, Double>();
		for (String v : graph.getVertices()) {
			System.out.println("Vertex : "+v+" Score:"+ranker.getVertexScore(v));
		}
		 
	}

	
	
}
