// A C++ implementation of running variance/standard deviation (Welford 1962)
// This follows http://www.johndcook.com/standard_deviation.html
// By brendan o'connor, anyall.org
// See main() on bottom for demo how to use
//     % g++ running_stat.cc
//     % ./a.out
//     added 0  now mean=0.00 var=0.00 std=0.00
//     added 1  now mean=0.50 var=0.25 std=0.50
//     added 2  now mean=1.00 var=0.67 std=0.82
//     added 3  now mean=1.50 var=1.25 std=1.12
//     added 4  now mean=2.00 var=2.00 std=1.41
//     added 5  now mean=2.50 var=2.92 std=1.71
//     added 6  now mean=3.00 var=4.00 std=2.00
//     added 7  now mean=3.50 var=5.25 std=2.29
//     added 8  now mean=4.00 var=6.67 std=2.58
//     added 9  now mean=4.50 var=8.25 std=2.87

#include <math.h>

class RunningStat {
  public:
    double s;
    double m;
    double last_m;
    unsigned int n;
    bool is_started;

    RunningStat() : s(0), m(0), last_m(0), n(0), is_started(false) {}
    void add(double x) {
      n++;
      if (!is_started) {
        m = x;
        s = 0;
        is_started = true;
      } else {
        last_m = m;
        m += (x - m) / n;
        s += (x - last_m) * (x-m);
      }
    }

    double var() { return s / n; }
    double std() { return sqrt(var()); }
    double mean() { return m; }

};



template <class T>
double running_var(T *x, unsigned int n)
{
  RunningStat rs;
  for (int i=0; i < n; i++) {
    rs.add( (double) x[i]);
  }
  return rs.var();
}

template <class T>
double running_std(T *x, unsigned int n)
{
  return sqrt(running_var_generic(x,n));
}


extern "C" {

double running_var_double(double *x, unsigned int n)
{
  return running_var(x, n);
}

double running_var_float(float *x, unsigned int n)
{
  return running_var(x, n);
}

}



#include <iostream>
#include <stdio.h>
using namespace std;


int main() {
  RunningStat rs;
  for (int i=0; i < 10; i++) {
    rs.add(i);
    printf("added %-2d now mean=%.2f var=%.2f std=%.2f\n", i,rs.mean(),rs.var(),rs.std());
  }
  cout << endl;

  // should get:
  //

  double x[10] = {0,1,2,3,4,5,6,7,8,9};
  cout << running_var(x,10) << endl;
  cout << running_var_double(x,10) << endl;


  float x2[10] = {0,1,2,3,4,5,6,7,8,9};
  cout << running_var(x2,10) << endl;


  int x3[10] = {0,1,2,3,4,5,6,7,8,9};
  cout << running_var(x3,10) << endl;
  return 0;
}

