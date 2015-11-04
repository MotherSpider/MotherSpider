package com.usc.solr.algos;

import java.io.BufferedReader;
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

import com.usc.solr.constatnts.Constants;
import com.usc.solr.graph.GraphUtil;
import com.usc.solr.model.Record;

import edu.uci.ics.jung.algorithms.scoring.PageRank;
import edu.uci.ics.jung.graph.DirectedSparseGraph;

/**
 * Class which implements Link Relevancy algorithm
 * 
 */
public class RelevancyAlgorithm {

	// Data strucutre to hold all records read from file
	static ArrayList<Record> allRecords = new ArrayList<Record>();

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
	public static void recordsToMap(Record rc) {

		allRecords.add(rc);
	}

	public ArrayList<Record> getAllRecords() {
		return allRecords;
	}

	public void setAllRecords(ArrayList<Record> allRecords) {
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
	 */
	public void fileToBean(String file) {
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

		try {
			BufferedReader br = new BufferedReader(new FileReader(file));
			while ((line = br.readLine()) != null) {

				if (line.startsWith("Recno")) {
					recordId = Integer.parseInt(line.split("::")[1].trim()
							.toLowerCase());

				}
				if (line.startsWith("URL")) {

					url = line.split("::")[1].trim();
					url = url.replace(" ", "");

				}
				if (line.startsWith("ParseText")) {
					line = br.readLine();
					if (!line.startsWith("#####")
							&& !line.startsWith("Content Metadata")) {
						parseText = line.trim().toLowerCase();

					}

				}

				if (line.startsWith("Content Metadata")) {

					contentMetadata = line.split("Content Metadata:")[1]
							.toLowerCase();

				}
				if (line.startsWith("LocationTag")) {

					location = line.split("LocationTag:")[1].toLowerCase();

				}
				if (line.startsWith("OrganizationTag")) {

					organization = line.split("OrganizationTag:")[1]
							.toLowerCase();

				}
				if (line.startsWith("PersonTag")) {

					person = line.split("PersonTag:")[1].toLowerCase();

				}
				if (line.startsWith("DateTag")) {

					date = line.split("DateTag:")[1].toLowerCase();

				}

				if (line.startsWith("#####")) {

					Record rc = new Record(recordId, url, parseText,
							contentMetadata, location, organization, person,
							date);
					recordId = 0;
					url = "";
					parseText = "";
					title = "";
					contentMetadata = "";
					location = "";
					organization = "";
					person = "";
					date = "";

					recordsToMap(rc);
				}
			}
			br.close();
		} catch (IOException e) {
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
	public void compareRecords(Record parent, GraphUtil myGraphUtil) {
		String[] parentLocations = parent.getLocation().trim().split(" ,");
		Set<String> pSetL = new HashSet<String>(Arrays.asList(parentLocations));
		String[] parentDates = parent.getDate().trim().split(" ,");
		Set<String> pSetD = new HashSet<String>(Arrays.asList(parentDates));
		String[] parentOrganization = parent.getOrganization().trim()
				.split(" ,");
		Set<String> pSetO = new HashSet<String>(
				Arrays.asList(parentOrganization));
		String[] parentPerson = parent.getPerson().trim().split(" ,");
		Set<String> pSetP = new HashSet<String>(Arrays.asList(parentPerson));

		String line = parent.getUrl();
		myGraphUtil.addToGraph(graph, seen, edgecount, line);

		for (Record rc : allRecords) {
			int matchFeat = 0;
			if (rc.getRecordId() > parent.getRecordId()) {
				// comparing all locations of child to parent
				String[] childLocations = rc.getLocation().trim().split(" ,");
				for (String lc : childLocations) {
					if (pSetL.contains(lc) && !lc.isEmpty()) {
						matchFeat++;
					}
				}
				// comparing all dates of child to parent
				String[] childDates = rc.getDate().trim().split(" ,");
				for (String dt : childDates) {
					if (pSetD.contains(dt) && !dt.isEmpty()) {
						matchFeat++;
					}
				}
				// comparing all organization of child to parent
				String[] childOrganization = rc.getOrganization().trim()
						.split(" ,");
				for (String org : childOrganization) {
					if (pSetO.contains(org) && !org.isEmpty()) {
						matchFeat++;
					}
				}
				// comparing all person of child to parent
				String[] childPerson = rc.getPerson().trim().split(" ,");
				for (String per : childPerson) {
					if (pSetP.contains(per) && !per.isEmpty()) {
						matchFeat++;
					}
				}
				if (matchFeat >= 1) {
					String line2 = parent.getUrl() + " " + rc.getUrl();

					myGraphUtil.addToGraph(graph, seen, edgecount, line2);
					edgecount = edgecount + 2;
					// wrt.write("{source: \""+parent.getUrl()+"\", target: \""+rc.getUrl()+"\", type: \"default\"},");
					// wrt.write("\n");
				}

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
			PrintWriter writer = new PrintWriter(
					Constants.OUTPUT_FILE_NAME_SCORES);
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
	
	public static void main(String args[]) throws FileNotFoundException {
		RelevancyAlgorithm myAlgo = new RelevancyAlgorithm();
		GraphUtil myGraphUtil = new GraphUtil();
		File folder = new File(Constants.INPUT_FILE_DIRECTORY);
		File[] listOfFiles = folder.listFiles();
		for (File file : listOfFiles) {

			myAlgo.fileToBean(Constants.INPUT_FILE_DIRECTORY + "/"
					+ file.getName());

		}
		// read inlink file
		String inline = "";

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

		for (Record rc : allRecords) {
			myAlgo.compareRecords(rc, myGraphUtil);
		}

		myGraphUtil.displayGraph(graph);
		System.out.println("Dumping Scores!!!");
		myAlgo.storeScore();
		System.out.println("Scores Dumped!!!");
	}

}
