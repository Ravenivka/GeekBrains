package Model;

import java.io.FileWriter;

public class Recorder {

    private String string;
    private String fileName;

    public Recorder(String value, String path) {
        this.string = value;
        this.fileName = path + ".txt";
    }

    public String Save() {
        try(FileWriter file = new FileWriter (this.fileName, true)){
            file.write(this.string);
            return String.format("Записано в %s", this.fileName);
        } catch (Exception e) {
            return e.getMessage();
        }
    }

}
