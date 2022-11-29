import java.util.Comparator;
import java.util.List;

/**
 * Institute: Radboud University
 * Course: SEM1V (AI: Principles & Techniques)
 * Student: Senna Renting (s1067489)
 * Task: 2
 * Date: 25 November 2022
 */

public class StandardOrder implements Comparator<List<Field>> {
    public int sort = 0;
    public int compare(List<Field> a, List<Field> b){
        sort++;
        return 0;
    }
}
