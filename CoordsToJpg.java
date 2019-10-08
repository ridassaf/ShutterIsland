import java.awt.*;
import java.awt.geom.AffineTransform;
import javax.swing.*;

import java.io.File;
import java.io.IOException;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.BufferedReader;
import java.io.FileReader;

public class CoordsToJpg{
	public static Color getColor(String col) {
		Color color = Color.WHITE;
		switch (col.toLowerCase()) {
			case "vlred":
				color = new Color(255,102,102);
				break;
			case "lred":
				color = new Color(255,51,51);
				break;
			case "red":
				color = new Color(255,0,0);
				break;
			case "dred":
				color = new Color(204,0,0);
				break;
			case "vlblue":
				color = new Color(51,204,255);
				break;
			case "lblue":
				color = new Color(51,153,255);
				break;
			case "blue":
				color = new Color(0,0,255);
				break;
			case "dblue":
				color = new Color(0,0,204);
				break;
			case "vlgreen":
				color = new Color(102,255,102);
				break;
			case "lgreen":
				color = new Color(0,255,51);
				break;
			case "green":
				color = new Color(0,255,0);
				break;
			case "dgreen":
				color = new Color(0,153,0);
				break;
			case "lyellow":
				color = new Color(255, 255, 153);
				break;
			case "yellow":
				color = new Color(255, 255, 0);
				break;
			case "dyellow":
				color = new Color(255, 204, 0);
				break;
			case "lorange":
				color = new Color(255, 153, 0);
				break;
			case "orange":
				color = new Color(255, 102, 0);
				break;
			case "gold":
				color = new Color(255, 204, 51);
				break;
			case "lgrey":
				color = new Color(204, 204, 204);
				break;
			case "dgrey":
				color = new Color(153, 153, 153);
				break;
			case "vdgrey":
				color = new Color(51, 51, 51);
				break;
			case "lbrown":
				color = new Color(153, 102, 0);
				break;
			case "dbrown":
				color = new Color(102, 0, 0);
				break;
			case "black":
				color = new Color(0, 0, 0);
				break;
			case "purple":
				color = new Color(102, 0, 153);
				break;
			case "maroon":
				color = new Color(153, 0,  0);
				break;
			case "salmon":
				color = new Color(255, 102, 102);
				break;
			case "magneta":
				color = Color.MAGENTA;
				break;
			case "magneta4":
				color = Color.MAGENTA.darker();
				break;
			default:
				System.out.println("Color " + col.toLowerCase() + " not found!");
		}
		return color;
	}
 

   public static  void saveImage() throws IOException {

	BufferedImage bufferedImage = new BufferedImage(300,300, BufferedImage.TYPE_INT_RGB);
	Graphics2D g2d = bufferedImage.createGraphics();

	int [] polygonXs = new int[7];
	int [] polygonYs = new int[7];
	Shape shape;
	File img_file;

	BufferedReader br = new BufferedReader(new FileReader("Coords/head_modified_xyc.txt"));
	String line;
	String img_name = "";
	String color = "";
	String [] xy = new String[2];
	while ((line = br.readLine()) != null) {
		if (line.charAt(0) == '>') {
			// for every new figure:
			g2d.setColor(Color.WHITE);
			g2d.fillRect(0, 0, 300, 300);
			img_name = line.substring(1);
		}

		// until we reach new figure
		while (color != null) { 
			br.mark(1000);
			color = br.readLine();
			if (color == null)
				break;
			if (color.charAt(0) == '>') {
				br.reset();
				break;
			}
			g2d.setColor(getColor(color));

			// Define an arrow shape using a polygon
			for (int i = 0; i < 7; i++) {
				xy = (br.readLine()).split("\t",2);
				polygonXs[i] = (int)Float.parseFloat(xy[0]);
				polygonYs[i] = (int)Float.parseFloat(xy[1]);
			}
			shape = new Polygon(polygonXs, polygonYs, polygonXs.length);
			g2d.fill(shape);
		}
		// when we reach new figure:
		img_file = new File("modified_images/"+ img_name + ".jpg");
		g2d.drawImage(bufferedImage, 0,0,null);
	       	ImageIO.write(bufferedImage, "jpg", img_file);
	}
   } 
   public static void main(String[] args) {
	try {
		saveImage();
	}
	catch (IOException ex) {
		System.out.println("IO Exception Caught!");
	}
   }
}
