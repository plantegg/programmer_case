import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.PreparedStatement;
public class Test { //不要琢磨代码规范、为什么要这么写，就是为了方便改吧改吧做很多不同的验证试验
    public static void main(String args[]) throws NumberFormatException, InterruptedException, ClassNotFoundException {
        Class.forName("com.mysql.jdbc.Driver");
        String url = args[0];
        String user = args[1];
        String pass = args[2];
        String sql = args[3];
        String interval = args[4];
        try {
            Connection conn = DriverManager.getConnection(url, user, pass);
            while (true) {
                PreparedStatement stmt = conn.prepareStatement(sql);
                //stmt.setFetchSize(Integer.MIN_VALUE); //这句是表示开流式读取，但是每条SQL 都会先发set net_write_timeout=600 给Server
                stmt.setString(1, interval);
                ResultSet rs = stmt.executeQuery();
                rs.close();
                stmt.close();

                PreparedStatement stmt2 = conn.prepareStatement(sql);
                stmt2.setString(1, interval);
                rs = stmt2.executeQuery();
								while (rs.next()) {
								    System.out.println("fine");
								}
                rs.close();
                stmt2.close();

                Thread.sleep(Long.valueOf(interval));
								break;
            }
						conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
