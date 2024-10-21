# Homework
1. The classification task is to predict if a student will pass the subject or
not. Check the website https://archive.ics.uci.edu/ml/datasets/
student+performance and analyze the list of attributes. Which of them
would you consider to be the most important? Choose 5-10 attributes,
which you will use in the experiments.
2. Open student-mat train and student-mat test.
3. Determine which metrics will be the most useful for this problem. Report
three the most accurate metrics.
4. Using J48 algorithm in Weka, restrict the list of attributes to the 5-10 attributes selected earlier and test a few different values of the parameters of
the algorithm (at least: confidenceFactor, minNumObj and binarySplits).
Show the results for each set of parameters (you can also visualize them).
Which set of parameter values yielded the best result for the test set?
5. Repeat the previous step, but this time use all of the attributes.
6. Load file student-por and run analysis for k = 10 in cross-validation.
Present your results.
7. Both datasets (math and Portuguese) have the same set of attributes.
Compare the structure of trees with the best results for each dataset.
Are there any similarities between them? Based on these results, can
we tell which attributes are the best predictors of whether the student is
attentive?
8. Choose any other algorithm that you already know e.g. algorithm for rule
induction that we used on the first laboratories (PRISM) or Naive Bayes
and run it on the student-mat dataset. Compare the results from both
algorithms. Which attributes had the biggest influence on the result? Are
these attributes similar to those that you chose intuitively at the beginning
of the task?

The task should be done in Weka.

The final report should be sent in a pdf format (other formats will not be
checked).
Your report must contain:
• for each set of parameters: a confusion matrix and values of the metrics
that you chose as the most accurate,
• charts that visualize how the change on each parameter influences the
results,
• the decision tree yielding the best results for each scenario (chosen attributes on math dataset, all attributes on math dataset, all attributes on
Portuguese dataset).
Time: + 2 weeks