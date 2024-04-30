/*
 * neural_network.h
 * Adapted from https://bitbucket.org/dimtass/machine-learning-for-embedded/src/master/
 */

#ifndef NEURAL_NETWORK_H_
#define NEURAL_NETWORK_H_

#ifdef __cplusplus
extern "C" {
#endif

double dot(double v[], double u[], int n);
double sigmoid(double x);

#ifdef __cplusplus
}
#endif

#endif /* NEURAL_NETWORK_H_ */
