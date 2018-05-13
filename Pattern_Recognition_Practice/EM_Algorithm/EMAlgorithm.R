library(mixtools)
library(dplyr)
library(ggplot2)

Epsilon = 1e-6

getFiniteSum <- function(x)
{
        sum(x[is.finite(x)])
}

getLogDnorm <- function(x, mu, sigma)
{
        getFiniteSum(sapply(x, function(x) {logdmvnorm(x, mu, sigma)})) 
}

EM <- function(data, maxIter)
{
        pi1 <- 0.5 # prior for class 1
        pi2 <- 0.5 # prior for class 2
        
        # set Initial values
        mu1 <- mean(data) * runif(1, 0.1, 1)
        mu2 <- mean(data) * runif(1, 0.1, 1)
        
        sigma1 <- var(data) * runif(1, 0.1, 1)
        sigma2 <- var(data) * runif(1, 0.1, 1)
        
        loglik <- rep(NA, 1000) # L(¥È)
        loglik[1] <- 0
        loglik[2] <- getFiniteSum(pi1 * (log(pi1) + getLogDnorm(data, mu1, sigma1))) + getFiniteSum(pi2 * (log(pi2) + getLogDnorm(data, mu2, sigma2)))
        
        tau1 <- 0
        tau2 <- 0
        
        k <- 2
        N <- length(data) # Number of samples
        
        # For compare
        gm<-normalmixEM(data,k=2,lambda=c(0.5,0.5),mu=c(mu1, mu2),sigma=c(sigma1, sigma2))
        
        print('==================== normalmixEM =====================')
        print(gm)
        
        
        # Loop
        while(abs(loglik[k] - loglik[k-1]) >= 0.00001)
        {
                # E-step
                tau1 <- pi1 * dnorm(data, mean=mu1, sd=sigma1)
                tau1 <- (tau1 / (pi1 * dnorm(data, mean=mu1, sd=sigma1) + pi2 * dnorm(data, mean=mu2, sd=sigma2)))
                tau2 <- pi2 * dnorm(data, mean=mu2, sd=sigma2)
                tau2 <- (tau2 / (pi1 * dnorm(data, mean=mu1, sd=sigma1) + pi2 * dnorm(data, mean=mu2, sd=sigma2)))
                
                # M-step
                # (1) calculate prior z
                pi1 <- getFiniteSum(tau1) / N;
                pi2 <- getFiniteSum(tau2) / N;
                
                # (2) calculate mu
                mu1 <- getFiniteSum(tau1 * data) / getFiniteSum(tau1)
                mu2 <- getFiniteSum(tau2 * data) / getFiniteSum(tau2)
                
                # (3) calculate sigma
                sigma1 <- getFiniteSum(tau1 * ((data - mu1)^2)) / getFiniteSum(tau1)
                sigma2 <- getFiniteSum(tau2 * ((data - mu2)^2)) / getFiniteSum(tau2)
                
                # to make non-zero
                sigma1 <- sigma1 + Epsilon
                sigma2 <- sigma2 + Epsilon
                
                loglik[k+1] <- getFiniteSum((log(pi1^tau1) + getLogDnorm(data, mu1, sigma1)^tau1)) + getFiniteSum((log(pi2^tau2) + getLogDnorm(data, mu2, sigma2)^tau2))
                #loglik[k+1] <- getFiniteSum(tau1 * (log(pi1) + getLogDnorm(data, mu1, sigma1))) + getFiniteSum(tau2 * (log(pi2) + getLogDnorm(data, mu2, sigma2)))
                #loglik[k+1] <- getFiniteSum(tau1 * (log(pi1) + log(dnorm(data, mu1, sigma1)))) + getFiniteSum(tau2 * (log(pi2) + log(dnorm(data, mu2, sigma2))))
                k<-k+1
        }

        list(mu = c(mu1, mu2), sigma = c(sqrt(sigma1), sqrt(sigma2)), pi = c(pi1, pi2), loglik = loglik[is.finite(loglik)])
}

#set.seed(0)
maxIter <- 100
heightData <- read.csv('https://raw.githubusercontent.com/BlackArbsCEO/Mixture_Models/K-Means%2C-E-M%2C-Mixture-Models/Class_heights.csv', stringsAsFactors=FALSE)

result <- EM(heightData$Height..in., 1000)

print('==================== My Algorithm =====================')
print(result)