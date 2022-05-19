import javax.swing.*;
import java.awt.*;
import java.text.*;
import java.util.*;
import java.net.*;
import java.io.*;
import javax.swing.text.AttributeSet;
import javax.swing.text.BadLocationException;
import javax.swing.text.PlainDocument;

public class GUI {
  static JLabel commandLabel;
  static IntegerDocument valueDocument;
  //Http client setup
  private static void createAndShowGUI() {
    Color backgroundColor = new Color(0, 0, 0);
    //Create and set up the window
    JFrame window = new JFrame("Robot App");
    window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    //Create a formatting frame to add buttons in a compass pattern
    JPanel mainPanel = new JPanel();
    GridLayout mainPanelLayout = new GridLayout(3, 3);
    mainPanelLayout.setHgap(10);
    mainPanelLayout.setVgap(10);
    mainPanel.setLayout(mainPanelLayout);
    mainPanel.setBackground(backgroundColor);
    mainPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
		
    //value container
    valueDocument = new IntegerDocument(5);

    //Command Label
    JPanel commandLabelPanel = new JPanel();
    commandLabelPanel.setLayout(new GridLayout(1,1));
    commandLabelPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
    commandLabelPanel.setBackground(backgroundColor);
    commandLabel = new JLabel();
    commandLabel.setText("Command Here");
    commandLabel.setForeground(new Color(255,255,255));
    commandLabelPanel.add(commandLabel);
    mainPanel.add(commandLabelPanel);

		//Forward Button
    JButton forwardButton = new JButton("Forward");
    forwardButton.addActionListener(e -> sendCommand("Forward", valueDocument.getValue()));
    forwardButton.setBackground(new Color(255, 255, 255));
    mainPanel.add(forwardButton);

    //Empty cell
    mainPanel.add(Box.createGlue());

		//Left Button
    JButton leftButton = new JButton("Left");
    leftButton.addActionListener(e -> sendCommand("Turn", -valueDocument.getValue()));
    leftButton.setBackground(new Color(255, 255, 255));
    mainPanel.add(leftButton);

		//value textbox
    JTextField valueField = new JTextField(1);
    valueField.setDocument(valueDocument);
    valueField.setHorizontalAlignment(JTextField.CENTER);
    valueField.setFont(new Font("SansSerif", Font.BOLD, 20));
    valueField.setBackground(new Color(150, 150, 150));
    valueField.setForeground(new Color(250, 250, 250));
    mainPanel.add(valueField);

		//Right Button
    JButton rightButton = new JButton("Right");
    rightButton.addActionListener(e -> sendCommand("Turn", valueDocument.getValue()));
    rightButton.setBackground(new Color(255, 255, 255));
    mainPanel.add(rightButton);

    //Empty cell
    mainPanel.add(Box.createGlue());

		//Backward Button
    JButton backwardButton = new JButton("Backward");
    backwardButton.addActionListener(e -> sendCommand("Forward", -valueDocument.getValue()));
    backwardButton.setBackground(new Color(255, 255, 255));
    mainPanel.add(backwardButton);

    //Auto Button
    JPanel autoPanel = new JPanel();
    autoPanel.setLayout(new GridLayout(1, 1));
    autoPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
    autoPanel.setBackground(backgroundColor);
    JButton autoButton = new JButton("Auto");
    autoButton.addActionListener(e -> sendCommand("Auto", 0));
    autoButton.setBackground(new Color(255, 255, 255));
    autoPanel.add(autoButton);
    mainPanel.add(autoPanel);

    //Display the window.
    window.getContentPane().add(mainPanel);
    window.pack();
    window.setSize(400, 400);
    window.setVisible(true);
  }

  private static class IntegerDocument extends PlainDocument {
    private int limit;

    IntegerDocument(int limit) {
    super();
    this.limit = limit;
    }

    public void insertString(int offset, String  str, AttributeSet attr ) throws BadLocationException {
      if (str == null) return;

      if ((getLength() + str.length()) <= limit) {
        try {
          Integer.parseInt(str);
          super.insertString(offset, str, attr);
        } catch(NumberFormatException e){
        }
      }
    }
    
    public int getValue() {
      if (super.getLength() == 0) {
        return 0;
      }
      try {
        return Integer.parseInt(super.getText(0, super.getLength()));
      } catch(Exception e){
        System.out.println("Failed document");
        System.out.println(e);
        return -1;
      }
    }
  }
  
  private static void sendCommand(String command, int value){
      if (command.equals("Auto")) {
        commandLabel.setText("<html><p>Running Auto</p></html>");
        sendGet("http://192.168.1.200:5000/control?command=Auto");
      } else {
        commandLabel.setText(String.format("<html><p>Running %s: %d</p></html>", command, value));
        sendGet(String.format("http://192.168.1.200:5000/control?command=%s&value=%d", command, value));
      }
  }

  private static void sendGet(String url){
    try {
      URL m_url = new URL(url);
      HttpURLConnection httpConnection = (HttpURLConnection) m_url.openConnection();
      httpConnection.getResponseCode();
    } catch (IOException e) {
      System.out.println("SendGet Failed to execute");
      System.out.println(e);
    };
  }

  public static void main(String[] args) {
    //Schedule a job for the event-dispatching thread:
    //creating and showing this application's GUI.
    javax.swing.SwingUtilities.invokeLater(new Runnable() {
      public void run() {
        createAndShowGUI();
      }
    });
  }
}
