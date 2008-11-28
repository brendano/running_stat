// A C++ implementation of running variance/standard deviation (Welford 1962)
// This follows http://www.johndcook.com/standard_deviation.html
// by brendan o'connor, anyall.org

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
using namespace std;

int main() {
  double x[10] = {0,1,2,3,4,5,6,7,8,9};
  cout << running_var(x,10) << endl;
  cout << running_var_double(x,10) << endl;


  float x2[10] = {0,1,2,3,4,5,6,7,8,9};
  cout << running_var(x2,10) << endl;


  int x3[10] = {0,1,2,3,4,5,6,7,8,9};
  cout << running_var(x3,10) << endl;
  return 0;
}

