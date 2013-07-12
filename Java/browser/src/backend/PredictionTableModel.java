package backend;

import javax.swing.table.DefaultTableModel;

public class PredictionTableModel extends DefaultTableModel {

	public static String[] COL_NAMES = {"HTID","Author","Title","Date","Page Start","Page End","Part Start","Part End","Prediction"};
	public static int HTID_COL = 0;
	public static int AUTHOR_COL = 1;
	public static int TITLE_COL = 2;
	public static int DATE_COL = 3;
	public static int PAGESTART_COL = 4;
	public static int PAGEEND_COL = 5;
	public static int PARTSTART_COL = 6;
	public static int PARTEND_COL = 7;
	public static int PREDICT_COL = 8;
	public static String DEFAULT_RANGE = "0";
	public static String DEFAULT_PART = "0";
	
	public PredictionTableModel() {
		setColumnIdentifiers(COL_NAMES);
	}

	public boolean isCellEditable(int row, int column) {
		return false;
	}
	
	public void addPrediction(String htid, String author, String title, String date, String prediction) {
		String[] row = new String[9];
		row[HTID_COL] = htid;
		row[AUTHOR_COL] = author;
		row[TITLE_COL] = title;
		row[DATE_COL] = date;
		row[PREDICT_COL] = prediction;
		row[PAGESTART_COL] = DEFAULT_RANGE;
		row[PAGEEND_COL] = DEFAULT_RANGE;
		row[PARTSTART_COL] = DEFAULT_PART;
		row[PARTEND_COL] = DEFAULT_PART;
		addRow(row);
	}
	
	public void addPrediction(String htid, String author, String title, String date, String pgstart, String pgend, String ptstart, String ptend, String prediction) {
		String[] row = new String[9];
		row[HTID_COL] = htid;
		row[AUTHOR_COL] = author;
		row[TITLE_COL] = title;
		row[DATE_COL] = date;
		row[PREDICT_COL] = prediction;
		row[PAGESTART_COL] = pgstart;
		row[PAGEEND_COL] = pgend;
		row[PARTSTART_COL] = ptstart;
		row[PARTEND_COL] = ptend;
		addRow(row);
	}
	
	
}
