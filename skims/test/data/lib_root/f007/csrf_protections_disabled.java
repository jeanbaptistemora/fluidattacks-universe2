import java.net.URI;
import java.net.URISyntaxException;
import java.util.Map;
import java.util.Properties;
import java.time.Duration;

public class MainApplication implements CommandLineRunner {

    public SecurityWebFilterChain springSecurityFilterChain(ServerHttpSecurity http) {
        http.csrf().ignoringAntMatchers("/route/");
        http.csrf().disable()
            .headers(headerCustomizer -> {
                headerCustomizer.xssProtection().disable();
                headerCustomizer.contentSecurityPolicy("frame-ancestors 'none'");
                headerCustomizer.hsts()
                    .includeSubdomains(true)
                    .maxAge(Duration.ofDays(365));
            });
        return http.build();
    }
}
