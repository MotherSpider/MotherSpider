package com.usc.solr.algos;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.usc.solr.constatnts.Constants;
import com.usc.solr.graph.GraphUtil;
import com.usc.solr.model.Record;
import com.usc.solr.model.Record38;

import edu.uci.ics.jung.algorithms.scoring.PageRank;
import edu.uci.ics.jung.graph.DirectedSparseGraph;

/**
 * Class which implements Link Relevancy algorithm
 * 
 */
public class WeaponsRelevancyAlgorithm {

	// Data strucutre to hold all records read from file
	static ArrayList<Record38> allRecords = new ArrayList<Record38>();

	// Graph to hold all records
	static DirectedSparseGraph<String, Integer> graph = new DirectedSparseGraph<String, Integer>();

	static HashSet<String> seen = new HashSet<String>();

	static int edgecount = 0;

	/**
	 * This method takes the Record bean and populates a ArrayList data
	 * structure accordingly.
	 * 
	 * @param rc
	 */
	public static void recordsToMap(Record38 rc) {

		allRecords.add(rc);
	}

	public ArrayList<Record38> getAllRecords() {
		return allRecords;
	}

	public void setAllRecords(ArrayList<Record38> allRecords) {
		this.allRecords = allRecords;
	}

	/**
	 * This method reads the file which contains the parsed text,feature tags
	 * and metadata and populates the record beans accordingly. Symbol #####
	 * Acts as record separator Format Expected of File: Recno:: 0 URL::
	 * http://about.gmu.edu/ ParseText:: Sample parsed text Content Metadata:
	 * Expires=Wed, 11 Jan 1984 05:00:00 GMT _fst_=33 ......... #####
	 * 
	 * @param file
	 * @throws ParseException 
	 */
	public void fileToBean(String file) throws ParseException {
		String line;
		int recordId = 0;
		String url = "";
		String parseText = "";
		String title = "";
		String contentMetadata = "";
		String location = "";
		String organization = "";
		String person = "";
		String date = "";
		// reading individual records from file and populating Record Bean
		Double lat=0.0;
		Double lon=0.0;
		try {
			JSONParser parser = new JSONParser();	  
			  Object obj = parser.parse(new FileReader(file));

			  JSONObject rec = (JSONObject) obj;
			  System.out.println(rec.get("url"));
			  
			  if(rec.get("url")!="")
			  {
			  
			  lat = (Double)rec.get("geonames_address.geo.lat");
			  lon = (Double)rec.get("geonames_address.geo.lon");
			  url= (String)rec.get("url");
			  if(lat!=null && lon!=null)
			  {
			  Long latTemp=Math.round((lat * 10)/10);
			  Long lonTemp=Math.round((lon * 10)/10);
			  
			    System.out.println(latTemp);
			    System.out.println(lonTemp);
					Record38 rc = new Record38(latTemp,lonTemp,url);
					lat=0.0;
					lon=0.0;

					recordsToMap(rc);
			  }
			  }
		}
		
	
		 catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	/**
	 * Method to compare all records with each other on basis of feature set and
	 * write to file in the format Source RelevantDoc1 RelevantDoc2
	 * 
	 * @param List
	 *            of all records
	 * 
	 */
	
	
	public void compareRecords(Record38 parent, GraphUtil myGraphUtil) {
		Long lat = parent.getLat();
		Long lon = parent.getLon();

		

		String line = parent.getUrl();
		myGraphUtil.addToGraph(graph, seen, edgecount, line);

		for (Record38 rc : allRecords) {
			int matchFeat = 0;
			

				// comparing all person of child to parent
			Long lat1 = rc.getLat();
			Long lon1 = rc.getLon();
					if (lat1==lat && lon1==lon) {
						matchFeat++;
					}
			
				if (matchFeat >= 1) {
					String line2 = parent.getUrl() + " " + rc.getUrl();

					myGraphUtil.addToGraph(graph, seen, edgecount, line2);
					edgecount = edgecount + 2;

				}

			}

	

	}
	

	/**
	 * method to store page rank score for each node in a file
	 */
	public void storeScore() {
		PageRank<String, Integer> ranker = new PageRank<String, Integer>(graph,
				0.15);
		ranker.evaluate();
		try {
			PrintWriter writer = new PrintWriter("/home/kshamakrishnan/Desktop/pageRankoutput.txt");
			for (String v : graph.getVertices()) {
				double score = ranker.getVertexScore(v);
				BigDecimal bd = new BigDecimal(score);
				writer.write(v.trim() + " " + bd + '\n');
			}
			writer.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	// Main method to test the algorithm .Reads the input file in specified format
	
	public static void main(String args[]) throws FileNotFoundException, ParseException {
		WeaponsRelevancyAlgorithm myAlgo = new WeaponsRelevancyAlgorithm();
		GraphUtil myGraphUtil = new GraphUtil();
		File folder = new File("/home/kshamakrishnan/Downloads/flattenedJson/");
		File[] listOfFiles = folder.listFiles();
		for (File file : listOfFiles) {

			myAlgo.fileToBean("/home/kshamakrishnan/Downloads/flattenedJson/"+file.getName());

		}
		// read inlink file
		String inline = "";
		/*
		try {
			BufferedReader br = new BufferedReader(new FileReader(
					Constants.INPUT_FILE_NAME_INLINKS));
			while ((inline = br.readLine()) != null) {
				myGraphUtil.addToGraph2(graph, seen, edgecount, inline);
				edgecount = edgecount + 1;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		// read outlink file
		try {
			BufferedReader br = new BufferedReader(new FileReader(
					Constants.INPUT_FILE_NAME_OUTLINKS));
			while ((inline = br.readLine()) != null) {
				myGraphUtil.addToGraph3(graph, seen, edgecount, inline);
				edgecount = edgecount + 1;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		*/
		
		for (Record38 rc : allRecords) {
			
			myAlgo.compareRecords(rc, myGraphUtil);
		}
		

		myGraphUtil.displayGraph(graph);
		
		System.out.println("Dumping Scores!!!");
		myAlgo.storeScore();
		System.out.println("Scores Dumped!!!");
		
	}

}
