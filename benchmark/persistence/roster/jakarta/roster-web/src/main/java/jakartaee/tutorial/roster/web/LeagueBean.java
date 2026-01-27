package jakartaee.tutorial.roster.web;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import jakarta.annotation.PostConstruct;
import jakarta.ejb.EJB;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.faces.application.FacesMessage;
import jakarta.faces.context.FacesContext;
import jakarta.inject.Named;
import jakarta.tutorial.roster.request.RequestBean;
import jakarta.tutorial.roster.util.LeagueDetails;
import jakarta.tutorial.roster.util.TeamDetails;

@Named
@ApplicationScoped
public class LeagueBean implements Serializable {
    
    @EJB
    private RequestBean requestBean;
    
    private List<LeagueDetails> leagues;
    private List<TeamDetails> teams;
    
    @PostConstruct
    public void init() {
        loadData();
    }
    
    public void loadData() {
        loadLeagues();
        loadTeams();
    }
    
    private void loadLeagues() {
        try {
            // Since there's no getAllLeagues method, we'll initialize with known league IDs
            // from the sample data: summer-league and winter-league
            leagues = new ArrayList<>();
            
            // Try to get the predefined leagues
            for (String leagueId : Arrays.asList("summer-league", "winter-league")) {
                try {
                    LeagueDetails league = requestBean.getLeague(leagueId);
                    if (league != null) {
                        leagues.add(league);
                    }
                } catch (Exception e) {
                    // League doesn't exist yet, that's okay
                }
            }
            
            // If no leagues exist, create them
            if (leagues.isEmpty()) {
                try {
                    LeagueDetails summerLeague = new LeagueDetails("summer-league", "Summer League", "soccer");
                    requestBean.createLeague(summerLeague);
                    leagues.add(summerLeague);
                    
                    LeagueDetails winterLeague = new LeagueDetails("winter-league", "Winter League", "soccer");
                    requestBean.createLeague(winterLeague);
                    leagues.add(winterLeague);
                } catch (Exception e) {
                    FacesContext.getCurrentInstance().addMessage(null,
                        new FacesMessage(FacesMessage.SEVERITY_ERROR, "Error creating leagues", e.getMessage()));
                }
            }
        } catch (Exception e) {
            FacesContext.getCurrentInstance().addMessage(null,
                new FacesMessage(FacesMessage.SEVERITY_ERROR, "Error loading leagues", e.getMessage()));
            leagues = new ArrayList<>();
        }
    }
    
    private void loadTeams() {
        try {
            teams = new ArrayList<>();
            // Get teams from all leagues
            for (LeagueDetails league : getLeagues()) {
                List<TeamDetails> leagueTeams = requestBean.getTeamsOfLeague(league.getId());
                if (leagueTeams != null) {
                    teams.addAll(leagueTeams);
                }
            }
        } catch (Exception e) {
            FacesContext.getCurrentInstance().addMessage(null,
                new FacesMessage(FacesMessage.SEVERITY_ERROR, "Error loading teams", e.getMessage()));
            teams = new ArrayList<>();
        }
    }
    
    public void clearCache() {
        leagues = null;
        teams = null;
        loadData();
    }
    
    public List<String> getLeagueIds() {
        List<String> ids = new ArrayList<>();
        for (LeagueDetails league : getLeagues()) {
            ids.add(league.getId());
        }
        return ids;
    }
    
    // Getters
    
    public List<LeagueDetails> getLeagues() {
        if (leagues == null) {
            loadLeagues();
        }
        return leagues;
    }
    
    public List<TeamDetails> getTeams() {
        if (teams == null) {
            loadTeams();
        }
        return teams;
    }
}
