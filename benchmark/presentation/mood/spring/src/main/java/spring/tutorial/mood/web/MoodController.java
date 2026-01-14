package spring.tutorial.mood.web;

import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import jakarta.servlet.http.HttpServletRequest;

@RestController
public class MoodController {

    @GetMapping(value = "/report", produces = MediaType.TEXT_HTML_VALUE)
    public String getReport(HttpServletRequest request,
                            @RequestParam(required = false, defaultValue = "") String name) {
        String mood = (String) request.getAttribute("mood");
        String person = name.isBlank() ? "friend" : name;

        // Produce the same HTML your servlet printed, including images now under /images/...
        return """
               <!doctype html>
               <html lang="en">
                 <head><meta charset="utf-8"><title>Mood Report</title></head>
                 <body>
                   <h1>Mood report</h1>
                   <p>Hello %s — current mood: <b>%s</b></p>
                   <img src="/images/duke.waving.gif" alt="duke waving">
                 </body>
               </html>
               """.formatted(person, mood);
    }

    @PostMapping(value = "/report", produces = MediaType.TEXT_HTML_VALUE)
    public String postReport(HttpServletRequest request,
                             @RequestParam(required = false, defaultValue = "") String name) {
        // Reuse the GET logic (your original servlet had doPost→processRequest)
        return getReport(request, name);
    }
}
