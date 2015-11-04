package com.usc.solr.model;

/**
 * Bean Class which holds individual records
 * 
 */
public class Record38 {

	Long lat;
	Long lon;
	String url;
	public String getUrl() {
		return url;
	}
	public void setUrl(String url) {
		this.url = url;
	}

	public Long getLat() {
		return lat;
	}
	public void setLat(Long lat) {
		this.lat = lat;
	}
	public Long getLon() {
		return lon;
	}
	public void setLon(Long lon) {
		this.lon = lon;
	}
	public Record38(Long lat,Long lon,String url)
	{
		this.lat=lat;
		this.lon=lon;
		this.url=url;
	}
	
	
	//int recordId;
	
	//String timestamp;
	//String category;
	//String buyer;
	
	

	
}
