/**
 * 
 */
package datamodel;
import java.util.ArrayList;

/**
 * @author tunderwood
 * 
 * In large part this class does the job of a Hadoop mapper:
 * sorting input lines into separate ArrayLists depending on
 * their keys. In reality, the Hadoop mapper would also have to
 * identify the "key" (which is the docid here), by extracting
 * it from the line of text received by the mapper. Here that
 * part of the mapping work is done by  BlockReader.
 * 
 */

public class GroupedSequence {
	ArrayList<ArrayList<String>> sequence;
	int memberCount;
	ArrayList<String> memberList;
	
	public GroupedSequence() {
		memberCount = 0;
		memberList = new ArrayList<String>();
		sequence = new ArrayList<ArrayList<String>>();
	}
	
	public void addLine(String key, String value) {
		if (memberList.contains(key)) {
			int idx = memberList.indexOf(key);
			// could implement this as a hash if you think performance matters
			ArrayList<String> thisMember = sequence.get(idx);
			thisMember.add(value);
			sequence.set(idx, thisMember);
		}
		else {
			ArrayList<String> newMember = new ArrayList<String>();
			newMember.add(value);
			memberCount += 1;
			memberList.add(key);
			sequence.add(newMember);
		}
		
	}
	
	public ArrayList<String> getMember(String memberLabel) {
		int idx = memberList.indexOf(memberLabel);
		return sequence.get(idx);
	}
	
}
