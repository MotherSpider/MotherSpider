package com.usc.solr.model;

/**
 * Bean Class which holds individual records
 * 
 */
public class Record {

	int recordId;
	String url;
	String parseText;
	String contentMetadata;
	String location;
	String organization;
	String person;
	String date;

	public String getDate() {
		return date;
	}

	public void setDate(String date) {
		this.date = date;
	}

	public Record(int recordId, String url, String parseText,
			String contentMetadata, String location,String organization,String person,String date) {
		this.recordId = recordId;
		this.url = url;
		this.parseText = parseText;
		this.contentMetadata = contentMetadata;
		this.location = location;
		this.organization=organization;
		this.person=person;
		this.date=date;
	}

	public int getRecordId() {
		return recordId;
	}

	public void setRecordId(int recordId) {
		this.recordId = recordId;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public String getParseText() {
		return parseText;
	}

	public void setParseText(String parseText) {
		this.parseText = parseText;
	}

	public String getContentMetadata() {
		return contentMetadata;
	}

	public void setContentMetadata(String contentMetadata) {
		this.contentMetadata = contentMetadata;
	}

	public String getLocation() {
		return location;
	}

	public void setLocation(String location) {
		this.location = location;
	}

	public String getOrganization() {
		return organization;
	}

	public void setOrganization(String organization) {
		this.organization = organization;
	}

	public String getPerson() {
		return person;
	}

	public void setPerson(String person) {
		this.person = person;
	}

}
