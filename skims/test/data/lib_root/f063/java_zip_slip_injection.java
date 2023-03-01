import java.io.File;
class zip_slip {
    public static List<String> zipSlipNoncompliant(ZipFile zipFile) throws IOException {
        Enumeration<? extends ZipEntry> entries = zipFile.entries();
        List<String> filesContent = new ArrayList<>();

        while (entries.hasMoreElements()) {
            ZipEntry entry = entries.nextElement();
            File file = new File(entry.getName());
            String content = FileUtils.readFileToString(file, StandardCharsets.UTF_8); // Noncompliant
            filesContent.add(content);
        }

        return filesContent;
    }

    public static List<String> zipSlipCompliant(ZipFile zipFile, String targetDirectory) throws IOException {
        Enumeration<? extends ZipEntry> entries = zipFile.entries();
        List<String> filesContent = new ArrayList<>();

        while (entries.hasMoreElements()) {
            ZipEntry entry = entries.nextElement();
            File file = new File(entry.getName());
            String canonicalDestinationPath = file.getCanonicalPath();

            if (!canonicalDestinationPath.startsWith(targetDirectory)) {
                throw new IOException("Entry is outside of the target directory");
            }

            String content = FileUtils.readFileToString(file, StandardCharsets.UTF_8); // Compliant
            filesContent.add(content);
        }

        return filesContent;
    }

    public static List<String> zipSlipCompliant2(String path, String targetDirectory) {
        File file = new File(pathFile);
        String content = FileUtils.readFileToString(file, StandardCharsets.UTF_8); // Compliant
        return content;
    }
}
