package gui;

import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.SQLException;
import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;

import backend.DerbyDB;
import backend.ResultsTableModel;

@SuppressWarnings("serial")
public class SearchBox extends JPanel {
    /**
     * This class takes data input from the user and passes it into the main DerbyDB
     * object as SQL queries.  The table model for SearchResults lives here as the
     * other class doesn't write to the table model.
     */

    private JLabel authorLabel,titleLabel,htidLabel,beforeLabel,afterLabel;
    private JTextField authorField,titleField,htidField,beforeField,afterField;
    private JPanel commands;
    private JButton submit, clear;
    private JCheckBox subset;
    ResultsTableModel resultsModel;

    // References to external data structures
    private final DerbyDB derby;

    // Search interface constants
    // final private String[] COL_NAMES = {"HTID","Author","Title","Date"};
    final private int MIN_SEARCH = 1;

    public SearchBox (DerbyDB conn) {
        /**
         * Basic constructor that requires an initialized (and successfully connected)
         * DerbyDB object. This reference is stored internally for use by this class'
         * private methods.
         */
        resultsModel = new ResultsTableModel();
        derby = conn;
        drawGUI();
        defineListeners();

    }

    private void drawGUI () {
        /**
         * Initializes all of the graphics objects and positions them within nested
         * panels/layout managers.  Panels used by groups are objects are initialized
         * in the same section as those objects.
         */

        GridBagConstraints labels,fields,full;
        setBorder(new EmptyBorder(10, 10, 5, 5));
        Dimension textbox = new Dimension(175,30);

        // Set universal layout properties
        setLayout(new GridBagLayout());
        full = new GridBagConstraints();
        full.gridwidth = 4;

        // Set universal label & form properties
        labels = new GridBagConstraints();
        labels.gridwidth = 1;
        labels.gridx = 0;
        fields = new GridBagConstraints();
        fields.gridwidth = 3;
        fields.gridx = 1;
        //fields.insets = new Insets(3,3,3,3);

        // Set remaining properties for each label and add to layout
        authorLabel = new JLabel("Author:");
        labels.gridy = 0;
        add(authorLabel,labels);
        titleLabel = new JLabel("Title:");
        labels.gridy = 1;
        add(titleLabel,labels);
        htidLabel = new JLabel("HTID:");
        labels.gridy = 2;
        add(htidLabel,labels);
        beforeLabel = new JLabel("Before:");
        labels.gridy = 3;
        add(beforeLabel,labels);
        afterLabel = new JLabel("After:");
        labels.gridy = 4;
        add(afterLabel,labels);

        // Set remaining properties for each form and add to layout
        authorField = new JTextField(null);
        authorField.setPreferredSize(textbox);
        fields.gridy = 0;
        add(authorField,fields);
        titleField = new JTextField(null);
        titleField.setPreferredSize(textbox);
        fields.gridy = 1;
        add(titleField,fields);
        htidField = new JTextField(null);
        htidField.setPreferredSize(textbox);
        fields.gridy = 2;
        add(htidField,fields);
        beforeField = new JTextField(null);
        beforeField.setPreferredSize(textbox);
        fields.gridy = 3;
        add(beforeField,fields);
        afterField = new JTextField(null);
        afterField.setPreferredSize(textbox);
        fields.gridy = 4;
        add(afterField,fields);

        // Create buttons in universal "full row" constraints but use nested grid for evenly split button sections
        full.gridx = 0;
        full.gridy = 5;
        subset = new JCheckBox("Limit search to predictions");
        add(subset,full);
        commands = new JPanel();
        commands.setLayout(new GridLayout(1,2));
        submit = new JButton("Search");
        clear = new JButton("Clear");
        commands.add(submit);
        commands.add(clear);
        full.gridy = 6;
        add(commands,full);
    }

    private void defineListeners() {
        /**
         * Sets all the button commands (ActionListeners).  This function creates them as
         * anonymous subclasses.  It's hacky, and for a bigger program it would probably
         * be better to define them each separately.  The overall function of each button
         * is described in comments preceding the ActionListener definitions.
         */

        submit.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                /**
                 * After checking to see if the search fields contain valid data, a SQL
                 * query is passed to DerbyDB.  Any results are added to the table model.
                 * If a SQL error is encountered here, it likely means that the database has
                 * been unexpectedly disconnected (which should only be a problem if
                 * DerbyDB is modified to work with remote databases).
                 */
                if (allowSearch()) {
                    String sql = buildSearchQuery(authorField.getText(),titleField.getText(),htidField.getText(),beforeField.getText(),afterField.getText(),subset.isSelected());
                    String[][] results;
                    try {
                        results = derby.query(sql);
                        for(int i=0;i<results.length;i++){
                            addRecord(results[i]);
                        }
                    } catch (SQLException badQuery) {
                        JOptionPane.showMessageDialog(null, "Database query cannot be processed.\n\nConsult derby.log for details.","Search Error",JOptionPane.WARNING_MESSAGE);
                    }
                } else {
                    JOptionPane.showMessageDialog(null, "Cannot perform search. Fields are empty or dates are not in expected format","Search Error",JOptionPane.PLAIN_MESSAGE);
                }
            }
        });

        clear.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                /**
                 * Clears all search fields and erases the data stored into the table.
                 */
                titleField.setText(null);
                authorField.setText(null);
                htidField.setText(null);
                afterField.setText(null);
                beforeField.setText(null);
                subset.setSelected(false);
                resultsModel.setRowCount(0);
            }
        });
    }

    private String buildSearchQuery (String author, String title, String htid, String before, String after, boolean limit) {
        /**
         * This method constructs a SQL query as a String to be passed to the Derby database.
         * Clauses are added together and inserted into a query template.
         */
        ArrayList<String> clauses = new ArrayList<String>();
        String query = "";
        String database;
        // Table selection
        if (limit) {
            database = "PREDICTION";
        } else {
            database = "COMPLETE";
        }
        // Clause builder
        if (author.trim().length() >= MIN_SEARCH) {
            clauses.add(" LOWER(AUTHOR) LIKE LOWER('%" + author + "%')");
        }
        if (title.trim().length() >= MIN_SEARCH) {
            clauses.add(" LOWER(TITLE) LIKE LOWER('%" + title + "%')");
        }

        if (htid.trim().length() >= MIN_SEARCH) {
            clauses.add(" LOWER(HTID) LIKE LOWER('%" + htid + "%')");
        }
        if (after.trim().length() == 4) {
            clauses.add(" DATE>=" + after.trim());
        }
        if (before.trim().length() == 4) {
            clauses.add(" DATE<=" + before.trim());
        }
        String[] builder = clauses.toArray(new String[clauses.size()]);
        for (int i=0;i<builder.length;i++){
            if (i>0){
                query += " AND";
            }
            query += builder[i];
        }
        return "SELECT HTID, TITLE, AUTHOR, DATE FROM " + database + " WHERE" + query + " ORDER BY DATE ASC";
    }

    private boolean allowSearch () {
        /**
         * Checks to see if the search fields have valid data (ie, dates are a full 4 digits
         * and that at least one field actually has text in it).
         */
        if ((beforeField.getText().length() != 4 && beforeField.getText().length() != 0) || (afterField.getText().length() != 4 && afterField.getText().length() != 0)) {
            return false;
        }
        else if (authorField.getText().length() < MIN_SEARCH && titleField.getText().length() < MIN_SEARCH && htidField.getText().length() < MIN_SEARCH) {
            return false;
        }
        else {
            return true;
        }
    }

    private void addRecord(String[] record) {
        /**
         * Adds a search result to the ResultsTableModel using that class's static
         * field indices.
         */
        resultsModel.addResult(record[ResultsTableModel.HTID_COL], record[ResultsTableModel.AUTHOR_COL], record[ResultsTableModel.TITLE_COL], record[ResultsTableModel.DATE_COL]);
    }

}
