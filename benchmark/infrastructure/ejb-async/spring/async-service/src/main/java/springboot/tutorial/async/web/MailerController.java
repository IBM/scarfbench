package springboot.tutorial.async.web;

import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.concurrent.Future;

import springboot.tutorial.async.ejb.MailerService;

@Controller
@Validated
public class MailerController {

    private static final String ATTR_FUTURE = "mailFuture";
    private static final String ATTR_STATUS = "mailStatus";

    @Autowired
    private MailerService mailerService;

    @GetMapping({"/thy", "/thy/index"})
    public String form(Model model, HttpSession session) {
        model.addAttribute("email", "");
        Object status = session.getAttribute(ATTR_STATUS);
        if (status != null) {
            model.addAttribute("status", status);
        }
        return "index"; // templates/index.html
    }

    @PostMapping("/thy/send")
    public String send(@RequestParam("email") String email, HttpSession session) {
        Future<String> future = mailerService.sendMessage(email);
        session.setAttribute(ATTR_FUTURE, future);
        session.setAttribute(ATTR_STATUS, "Processing... (refresh to check again)");
        return "redirect:/thy/response";
    }

    @GetMapping("/thy/response")
    public String response(Model model, HttpSession session) {
        @SuppressWarnings("unchecked")
        Future<String> future = (Future<String>) session.getAttribute(ATTR_FUTURE);
        String status = (String) session.getAttribute(ATTR_STATUS);
        if (future != null && future.isDone()) {
            try {
                status = future.get();
            } catch (Exception e) {
                status = e.getMessage();
            }
            session.setAttribute(ATTR_STATUS, status);
        }
        model.addAttribute("status", status);
        return "response"; // templates/response.html
    }
}
