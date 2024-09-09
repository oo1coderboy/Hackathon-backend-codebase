const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();
const port = 5000;


// Use CORS middleware
app.use(cors());
// Setup Multer for file uploads
const upload = multer({ dest: "uploads/" });

app.post("/upload", upload.single("file"), async (req, res) => {
  const file = req.file;
  const options = JSON.parse(req.body.options);

  if (!file) {
    return res.status(400).send("No file uploaded.");
  }

  // Define paths
  const inputFilePath = path.join(__dirname, "uploads", file.filename);
  const outputFileName = "anonymized_docx.docx"; // Or dynamically generate based on requirement
  const variablesPath = path.join(__dirname, "Team_Black_Code", "variables.py");
  const anonymizedFilePath = path.join(__dirname, outputFileName);

  // Ensure the anonymized_files directory exists
  if (!fs.existsSync(path.join(__dirname, "anonymized_files"))) {
    fs.mkdirSync(path.join(__dirname, "anonymized_files"));
  }

  // Update variables.py
  const variablesContent = `
input_file_path = r"${inputFilePath}" # ENTER INPUT FILE PATH
output_file_name = "${outputFileName}" # ENTER OUTPUT FILE NAME
pii_tags = ${JSON.stringify(
    options
  )} # if send empty, all tags from default_tags_list below will be anonymized
  `;
  fs.writeFileSync(variablesPath, variablesContent, "utf8");

  // Run pii_anonymizer.py
  exec(
    `python ${path.join(__dirname, "Team_Black_Code", "pii_anonymizer.py")}`,
    (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing script: ${error.message}`);
        return res.status(500).send(`Error executing script: ${error.message}`);
      }
      if (stderr) {
        console.error(`Script stderr: ${stderr}`);
        return res.status(500).send(`Script stderr: ${stderr}`);
      }

      // Send the anonymized file back to the client
      res.download(anonymizedFilePath, outputFileName, (err) => {
        if (err) {
          console.error(`Error sending file: ${err.message}`);
          return res.status(500).send(`Error sending file: ${err.message}`);
        }

        // Clean up uploaded file if necessary
        fs.unlinkSync(inputFilePath);
      });
    }
  );
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
