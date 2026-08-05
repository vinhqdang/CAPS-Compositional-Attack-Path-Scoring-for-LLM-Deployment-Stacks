\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{BVP_MS-NEW}
              [2024/06/05 v1.5m
 Standard LaTeX document class]
% \newcommand\@ptsize{}
% \newif\if@restonecol
% \newif\if@titlepage
% \@titlepagefalse
% \if@compatibility\else
%   \DeclareOption{a4paper}
%      {\setlength\paperheight {297mm}%
%       \setlength\paperwidth  {210mm}}
%   \DeclareOption{a5paper}
%      {\setlength\paperheight {210mm}%
%       \setlength\paperwidth  {148mm}}
%   \DeclareOption{b5paper}
%      {\setlength\paperheight {250mm}%
%       \setlength\paperwidth  {176mm}}
%   \DeclareOption{letterpaper}
%      {\setlength\paperheight {11in}%
%       \setlength\paperwidth  {8.5in}}
%   \DeclareOption{legalpaper}
%      {\setlength\paperheight {14in}%
%       \setlength\paperwidth  {8.5in}}
%   \DeclareOption{executivepaper}
%      {\setlength\paperheight {10.5in}%
%       \setlength\paperwidth  {7.25in}}
%   \DeclareOption{landscape}
%      {\setlength\@tempdima   {\paperheight}%
%       \setlength\paperheight {\paperwidth}%
%       \setlength\paperwidth  {\@tempdima}}
% \fi
% \if@compatibility
%   \renewcommand\@ptsize{0}
% \else
%   \DeclareOption{10pt}{\renewcommand\@ptsize{0}}
% \fi
% \DeclareOption{11pt}{\renewcommand\@ptsize{1}}
% \DeclareOption{12pt}{\renewcommand\@ptsize{2}}
% \if@compatibility\else
%   \DeclareOption{oneside}{\@twosidefalse \@mparswitchfalse}
% \fi
% \DeclareOption{twoside}{\@twosidetrue  \@mparswitchtrue}
% \DeclareOption{draft}{\setlength\overfullrule{5pt}}
% \if@compatibility\else


\newcount\affilcount\affilcount0
\newcount\affiltempcount
\newcount\tempaffilcount
\newcount\afflabcnt

\newcounter{figure}
\newcounter{table}

\newbox\figcapbox
\newbox\figtempbox
\newbox\tabcapbox
\newbox\tabbox
\newbox\tabnotebox
\newbox\tablefootbox

\newskip\figcaptionleftskip
\newskip\figcaptionrightskip
\newskip\figleftskip
\newskip\figrightskip
\newskip\adjustskip
\newskip\sidetskip\sidetskip=0pt
\newskip\sideverticalskip\sideverticalskip=0pt
\newskip\fignumcapsep\fignumcapsep=3pt
\newskip\figcapdescsep\figcapdescsep=2.5pt
\newskip\tableleftskip%
\newskip\tablerightskip%
\newskip\tablecapleftskip%
\newskip\tablecaprightskip%
\newskip\sideverticalskip
\newskip\sidetskip
\newskip\addtotablewidth
\newskip\tablenumcapsep
\newskip\tablefootleftskip
\newskip\tablefootrightskip

\newdimen\toprulewidth
\newdimen\midrulewidth
\newdimen\botrulewidth
\newdimen\cmidrulewidth
\newdimen\belowrulesep
\newdimen\belowbottomsep
\newdimen\aboverulesep
\newdimen\abovetopsep
\newdimen\cmidrulesep
\newdimen\cmidrulekern
\newdimen\defaultaddspace
\newdimen\@thisrulewidth


\@twosidetrue

\newbox\abstractbox%
\newbox\keywordsbox


\DeclareOption{final}{\setlength\overfullrule{0pt}}
% \fi

% \DeclareOption{titlepage}{\@titlepagetrue}
% \if@compatibility\else
%   \DeclareOption{notitlepage}{\@titlepagefalse}
% \fi
% \if@compatibility\else
%   \DeclareOption{onecolumn}{\@twocolumnfalse}
% \fi
% \DeclareOption{twocolumn}{\@twocolumntrue}
% \DeclareOption{leqno}{\input{leqno.clo}}
% \DeclareOption{fleqn}{\input{fleqn.clo}}
% \DeclareOption{openbib}{%
%   \AtEndOfPackage{%
%     \renewcommand\@openbib@code{%
%       \advance\leftmargin\bibindent
%       \itemindent -\bibindent
%       \listparindent \itemindent
%       \parsep \z@
%       }%
%     \renewcommand\newblock{\par}}%
% }

% \newif\ifAAES\global\AAESfalse %- Archives of Advanced Engineering Science
% \newif\ifMEDIN\global\MEDINfalse %- Medinformatics
% \newif\ifAIA\global\AIAfalse %- Artificial Intelligence and Applications
% \newif\ifGLCE\global\GLCEfalse %- Green and Low-Carbon Economy
% \newif\ifIJCE\global\IJCEfalse %- International Journal of Changes in Education
% \newif\ifJCBAR\global\JCBARfalse %- Journal of Comprehensive Business Administration Research
% \newif\ifJCCE\global\JCCEfalse %- Journal of Computational and Cognitive Engineering
% \newif\ifJDSIS\global\JDSISfalse %- Journal of Data Science and Intelligent Systems
% \newif\ifJOPR\global\JOPRfalse %- Journal of Optics and Photonics Research


\setlength\paperheight{297mm}%
\setlength\paperwidth{210mm}

% \DeclareOption*{\PassOptionsToClass{\CurrentOption}{natbib}}
% \DeclareOption{AAES}{\global\AAEStrue}
% \DeclareOption{MEDIN}{\global\MEDINtrue}
% \DeclareOption{AIA}{\global\AIAtrue}
% \DeclareOption{GLCE}{\global\GLCEtrue}
% \DeclareOption{IJCE}{\global\IJCEtrue}
% \DeclareOption{JCBAR}{\global\JCBARtrue}
% \DeclareOption{JCCE}{\global\JCCEtrue}
% \DeclareOption{JDSIS}{\global\JDSIStrue}
% \DeclareOption{JOPR}{\global\JOPRtrue}


\ExecuteOptions{final}
\ProcessOptions


\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}


\renewcommand{\rmdefault}{ptm}
\renewcommand{\sfdefault}{phv}

\RequirePackage{ifpdf}
\RequirePackage{etex}
\RequirePackage{amsthm}
\RequirePackage{soul}
\RequirePackage{calc}
\RequirePackage{color}

%\def\FontI{ptm}%
%\def\FontII{phv}%
% \def\FontI{pad}%
% \def\FontII{9hn}%

\def\FontI{ptm}
\def\FontII{phv}



\RequirePackage{marginnote}
%\RequirePackage[T1,mtbold]{CLP-LaTeX-Mathfont}
\RequirePackage{mathptmx}
\renewcommand{\rmdefault}{ptm}
%\usepackage[italic]{mathastext}
\RequirePackage{fnpos,makeidx,ifthen,multicol}
\RequirePackage{textcomp}%Commented algorithm package for line numbers
%\RequirePackage{CLP-Pagegrid}
\RequirePackage{amsbsy}[1995/01/20]
\RequirePackage{amssymb}
\RequirePackage{amsmath}
% \RequirePackage{graphics}
\RequirePackage{graphicx}
\RequirePackage{ifthen}
\RequirePackage{color}
% \RequirePackage{ifthen}
\RequirePackage{calc}
% \RequirePackage{multicol}
% \RequirePackage{algorithm}
\RequirePackage{stfloats}
\RequirePackage{wrapfig}
% \RequirePackage{lipsum}
% \RequirePackage{cuted}
\RequirePackage{url}
\RequirePackage{etoolbox}
\RequirePackage{eurosym}
\RequirePackage{upgreek}
%\AtEndOfClass{

\def\email#1{\href{mailto:#1}{#1}}

%\RequirePackage{natbib}  % [super,square,comma,sort&compress]
\RequirePackage{hyperref}%
\hypersetup{
draft=false,
%dvips,
pdftex,%
%pdfpagemode=UseNone,
bookmarks=false,
%bookmarksopenlevel=3,
%bookmarksopen=true,
pdfborderstyle={/S/U/W 0},
pdfstartview={FitH 800},
breaklinks=true}
%}

% \def\titlefont{\fontencoding{T1}\fontfamily{phv}\fontseries{b}\fontsize{19}{26}\selectfont\raggedright}
% \def\authorfont{\fontfamily{\sfdefault}\fontseries{bc}\fontsize{11}{16}\selectfont\bfseries\raggedright\mathversion{bold}}
% \def\affilfont{\fontfamily{\sfdefault}\fontseries{c}\fontsize{9}{10.8}\selectfont\raggedright}
% \def\correspfont{\akrobatNine}
% \def\historyfont{\akrobatNine}
%\def\abstractfont{\fontsize{10}{12}\selectfont\bfseries\mathversion{bold}\leftskip24pt\rightskip24pt}
%\def\abstractfont{\fontfamily{\sfdefault}\fontsize{11}{14}\selectfont\mathversion{bold}\leftskip24pt\rightskip17pt}
%\def\akrobatNine{\fontfamily{\sfdefault}\fontseries{c}\fontsize{9}{10.8}\selectfont\raggedright}
%\def\akrobatElevenBold{\fontfamily{\sfdefault}\fontsize{11}{12}\selectfont\bfseries\raggedright}

%% section
% \def\paragraphfont{\itshape}%
% \def\subparagraphfont{}%
% \def\subsubparagraphfont{}%
%
\def\sectionnumfont{\sectionfont}
\def\subsectionnumfont{\subsectionfont}
%

%% figure
\def\figcaptionfont{\fontfamily{\rmdefault}\fontseries{b}\fontsize{9}{11}\selectfont\mathversion{bold}}
\def\figcaptiondescfont{\fontfamily{\rmdefault}\fontsize{9}{11}\selectfont} %}%\leftskip0pt plus1fill\rightskip0pt plus1fill}
\def\figcaptionnumfont{\fontfamily{\rmdefault}\fontseries{b}\fontsize{9}{11}\selectfont}

% %% TABLE
% %\def\multilistfont{\fontsize{8.5}{10}\selectfont\leftskip\tableleftskip\rightskip\tablerightskip}%
% %\def\multilistheadfont{\fontsize{8.5}{10}\bfseries\selectfont\leftskip\tableleftskip\rightskip\tablerightskip}%
% \def\tablefont{\fontfamily{\rmdefault}\fontsize{8.5}{10}\selectfont} %}%
% \def\tablecaptionfont{\fontfamily{\rmdefault}\fontseries{b}\mathversion{bold}\fontsize{9}{11}\selectfont} %}%
% \def\tablecaptwofont{\fontfamily{\rmdefault}\fontsize{9}{11}\selectfont} %}%
% \def\tablecaptionnumfont{\fontfamily{\rmdefault}\fontseries{b}\fontsize{9}{9}\selectfont} %}%
% \def\TCHfont{\fontfamily{\rmdefault}\fontsize{8.5}{10}\selectfont}%
% %\def\tbodyfont{\fontfamily{\sfdefault}\fontsize{9}{12}\selectfont}
% \def\tbodyfont{\fontfamily{\rmdefault}\fontsize{8.5}{10}\selectfont}
% %\def\mycr{\@xnewline\vskip4pt }
% \def\mycr{\crcr\noalign{\kern2\p@\global\let\cr\endline\vskip4pt}}
% \def\TSCHfont{}%
% \def\tabnotefont{\fontfamily{\rmdefault}\fontsize{7}{9}\selectfont}% use plus 1fill if needed

%%%

\definecolor{graysixty}{cmyk}{0,0,0,0.6}

\def\arttypefont{\fontfamily{\sfdefault}\fontsize{10}{12}\selectfont\bfseries}
\def\titlefont{\fontencoding{T1}\fontfamily{\rmdefault}\fontsize{17}{25}\bfseries\selectfont\raggedright}
\def\authorfont{\fontfamily{\rmdefault}\fontsize{10}{12}\bfseries\selectfont}
\def\affilfont{\fontfamily{\rmdefault}\fontsize{10}{12}\selectfont\itshape}
%\def\kwdfont{\fontfamily{\rmdefault}\fontsize{12}{20}\selectfont\leftskip19.5pt\rightskip19.5pt}
\def\kwdfont{\fontfamily{\rmdefault}\fontsize{9}{11}\selectfont}
\def\abstractfont{\fontfamily{\rmdefault}\fontsize{9}{11}\selectfont}
\def\historyfont{\fontfamily{\rmdefault}\fontsize{10}{12}\selectfont\centering}
\def\doifont#1{\textcolor{graysixty}{\fontfamily{\sfdefault}\fontsize{7}{8}\selectfont #1}}

%% section
\def\sectionfont{\fontfamily{\rmdefault}\fontsize{11}{13}\bfseries\mathversion{bold}\selectfont\rightskip0pt plus1fill}%
\def\subsectionfont{\fontfamily{\rmdefault}\fontsize{11}{13}\selectfont\bfseries\mathversion{bold}\rightskip0pt plus1fill} %
\def\subsubsectionfont{\fontfamily{\rmdefault}\fontsize{9}{11}\selectfont\selectfont\itshape\rightskip0pt plus1fill} %
\def\paragraphfont{\itshape}%
\def\subparagraphfont{}%
\def\subsubparagraphfont{}%
%
%% figure
\def\figcaptionfont{\fontfamily{\rmdefault}\fontseries{b}\fontsize{9}{11}\selectfont\mathversion{bold}}
\def\figcaptiondescfont{\fontfamily{\rmdefault}\fontsize{9}{11}\selectfont} %}%\leftskip0pt plus1fill\rightskip0pt plus1fill}
\def\figcaptionnumfont{\fontfamily{\rmdefault}\fontseries{b}\fontsize{9}{11}\selectfont}

%% TABLE
%\def\multilistfont{\fontsize{8.5}{10}\selectfont\leftskip\tableleftskip\rightskip\tablerightskip}%
%\def\multilistheadfont{\fontsize{8.5}{10}\bfseries\selectfont\leftskip\tableleftskip\rightskip\tablerightskip}%
\def\tablefont{\fontfamily{\rmdefault}\fontsize{8.5}{10}\selectfont} %}%
\def\tablecaptionfont{\fontfamily{\rmdefault}\fontseries{b}\mathversion{bold}\fontsize{9}{11}\selectfont} %}%
\def\tablecaptwofont{\fontfamily{\rmdefault}\fontsize{9}{11}\selectfont} %}%
\def\tablecaptionnumfont{\fontfamily{\rmdefault}\fontseries{b}\fontsize{9}{9}\selectfont} %}%
\def\TCHfont{\fontfamily{\rmdefault}\fontsize{8.5}{10}\selectfont}%
%\def\tbodyfont{\fontfamily{\sfdefault}\fontsize{9}{12}\selectfont}
\def\tbodyfont{\fontfamily{\rmdefault}\fontsize{8.5}{10}\selectfont}
%\def\mycr{\@xnewline\vskip4pt }
\def\mycr{\crcr\noalign{\kern2\p@\global\let\cr\endline\vskip4pt}}
\def\TSCHfont{}%
\def\tabnotefont{\fontfamily{\rmdefault}\fontsize{7}{9}\selectfont}% use plus 1fill if needed

\newenvironment{tabnote}%
{\begingroup\begin{minipage}{\hsize}\footnotesize\noindent}
{\end{minipage}\endgroup}

\renewcommand\normalsize{%
   \@setfontsize\normalsize\@ixpt\@xipt
   \abovedisplayskip 10\p@ \@plus2\p@ \@minus5\p@
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
   \belowdisplayskip \abovedisplayskip
   \let\@listi\@listI}
\normalsize
\newcommand\small{%
   \@setfontsize\small\@ixpt{11}%
   \abovedisplayskip 8.5\p@ \@plus3\p@ \@minus4\p@
   \abovedisplayshortskip \z@ \@plus2\p@
   \belowdisplayshortskip 4\p@ \@plus2\p@ \@minus2\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 4\p@ \@plus2\p@ \@minus2\p@
               \parsep 2\p@ \@plus\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}
\newcommand\footnotesize{%
   \@setfontsize\footnotesize\@viiipt{9.5}%
   \abovedisplayskip 6\p@ \@plus2\p@ \@minus4\p@
   \abovedisplayshortskip \z@ \@plus\p@
   \belowdisplayshortskip 3\p@ \@plus\p@ \@minus2\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 3\p@ \@plus\p@ \@minus\p@
               \parsep 2\p@ \@plus\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}
\newcommand\scriptsize{\@setfontsize\scriptsize\@viipt\@viiipt}
\newcommand\tiny{\@setfontsize\tiny\@vpt\@vipt}
\newcommand\large{\@setfontsize\large\@xiipt{14}}
\newcommand\Large{\@setfontsize\Large\@xivpt{18}}
\newcommand\LARGE{\@setfontsize\LARGE\@xviipt{22}}
\newcommand\huge{\@setfontsize\huge\@xxpt{25}}
\newcommand\Huge{\@setfontsize\Huge\@xxvpt{30}}
\if@twocolumn
  \setlength\parindent{1em}
\else
  \setlength\parindent{15\p@}
\fi
\setlength\smallskipamount{3\p@ \@plus 1\p@ \@minus 1\p@}
\setlength\medskipamount{6\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\bigskipamount{12\p@ \@plus 4\p@ \@minus 4\p@}
% \setlength\headheight{12\p@}
% \setlength\headsep   {25\p@}
% \setlength\topskip   {10\p@}
%\setlength\footskip{17\p@}
%\if@compatibility \setlength\maxdepth{4\p@} \else
\setlength\maxdepth{.5\topskip} %\fi
% \if@compatibility
%   \if@twocolumn
%     \setlength\textwidth{410\p@}
%   \else
%     \setlength\textwidth{345\p@}
%   \fi
% \else
%   \setlength\@tempdima{\paperwidth}
%   \addtolength\@tempdima{-2in}
%   \setlength\@tempdimb{345\p@}
%   \if@twocolumn
%     \ifdim\@tempdima>2\@tempdimb\relax
%       \setlength\textwidth{2\@tempdimb}
%     \else
%       \setlength\textwidth{\@tempdima}
%     \fi
%   \else
%     \ifdim\@tempdima>\@tempdimb\relax
%       \setlength\textwidth{\@tempdimb}
%     \else
%       \setlength\textwidth{\@tempdima}
%     \fi
%   \fi
% \fi
% \if@compatibility\else
%   \@settopoint\textwidth
% \fi
% \if@compatibility
%   \setlength\textheight{43\baselineskip}
% \else
%   \setlength\@tempdima{\paperheight}
%   \addtolength\@tempdima{-2in}
%   \addtolength\@tempdima{-1.5in}
%   \divide\@tempdima\baselineskip
%   \@tempcnta=\@tempdima
%   \setlength\textheight{\@tempcnta\baselineskip}
% \fi
% \addtolength\textheight{\topskip}
% \if@twocolumn
%   \setlength\marginparsep {10\p@}
% \else
%   \setlength\marginparsep{11\p@}
% \fi
% \setlength\marginparpush{5\p@}
% \if@compatibility
%   \if@twoside
%      \setlength\oddsidemargin   {44\p@}
%      \setlength\evensidemargin  {82\p@}
%      \setlength\marginparwidth {107\p@}
%   \else
%      \setlength\oddsidemargin   {63\p@}
%      \setlength\evensidemargin  {63\p@}
%      \setlength\marginparwidth  {90\p@}
%   \fi
%   \if@twocolumn
%      \setlength\oddsidemargin  {30\p@}
%      \setlength\evensidemargin {30\p@}
%      \setlength\marginparwidth {48\p@}
%   \fi
% \else
%   \if@twoside
%     \setlength\@tempdima        {\paperwidth}
%     \addtolength\@tempdima      {-\textwidth}
%     \setlength\oddsidemargin    {.4\@tempdima}
%     \addtolength\oddsidemargin  {-1in}
%     \setlength\marginparwidth   {.6\@tempdima}
%     \addtolength\marginparwidth {-\marginparsep}
%     \addtolength\marginparwidth {-0.4in}
%   \else
%     \setlength\@tempdima        {\paperwidth}
%     \addtolength\@tempdima      {-\textwidth}
%     \setlength\oddsidemargin    {.5\@tempdima}
%     \addtolength\oddsidemargin  {-1in}
%     \setlength\marginparwidth   {.5\@tempdima}
%     \addtolength\marginparwidth {-\marginparsep}
%     \addtolength\marginparwidth {-0.4in}
%     \addtolength\marginparwidth {-.4in}
%   \fi
%   \ifdim \marginparwidth >2in
%      \setlength\marginparwidth{2in}
%   \fi
%   \@settopoint\oddsidemargin
%   \@settopoint\marginparwidth
%   \setlength\evensidemargin  {\paperwidth}
%   \addtolength\evensidemargin{-2in}
%   \addtolength\evensidemargin{-\textwidth}
%   \addtolength\evensidemargin{-\oddsidemargin}
%   \@settopoint\evensidemargin
% \fi
% \if@compatibility
%   \setlength\topmargin{27pt}
% \else
%   \setlength\topmargin{\paperheight}
%   \addtolength\topmargin{-2in}
%   \addtolength\topmargin{-\headheight}
%   \addtolength\topmargin{-\headsep}
%   \addtolength\topmargin{-\textheight}
%   \addtolength\topmargin{-\footskip}     % this might be wrong!
%   \addtolength\topmargin{-.5\topmargin}
%   \@settopoint\topmargin
% \fi
\setlength\footnotesep{6.65\p@}
\setlength{\skip\footins}{9\p@ \@plus 4\p@ \@minus 2\p@}
\setlength\floatsep    {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\textfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\intextsep   {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dblfloatsep    {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dbltextfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\@fptop{0\p@ \@plus 1fil}
\setlength\@fpsep{8\p@ \@plus 2fil}
\setlength\@fpbot{0\p@ \@plus 1fil}
\setlength\@dblfptop{0\p@ \@plus 1fil}
\setlength\@dblfpsep{8\p@ \@plus 2fil}
\setlength\@dblfpbot{0\p@ \@plus 1fil}
\setlength\partopsep{2\p@ \@plus 1\p@ \@minus 1\p@}
\def\@listi{\leftmargin\leftmargini
            \parsep 4\p@ \@plus2\p@ \@minus\p@
            \topsep 8\p@ \@plus2\p@ \@minus4\p@
            \itemsep4\p@ \@plus2\p@ \@minus\p@}
\let\@listI\@listi
\@listi
\def\@listii {\leftmargin\leftmarginii
              \labelwidth\leftmarginii
              \advance\labelwidth-\labelsep
              \topsep    4\p@ \@plus2\p@ \@minus\p@
              \parsep    2\p@ \@plus\p@  \@minus\p@
              \itemsep   \parsep}
\def\@listiii{\leftmargin\leftmarginiii
              \labelwidth\leftmarginiii
              \advance\labelwidth-\labelsep
              \topsep    2\p@ \@plus\p@\@minus\p@
              \parsep    \z@
              \partopsep \p@ \@plus\z@ \@minus\p@
              \itemsep   \topsep}
\def\@listiv {\leftmargin\leftmarginiv
              \labelwidth\leftmarginiv
              \advance\labelwidth-\labelsep}
\def\@listv  {\leftmargin\leftmarginv
              \labelwidth\leftmarginv
              \advance\labelwidth-\labelsep}
\def\@listvi {\leftmargin\leftmarginvi
              \labelwidth\leftmarginvi
              \advance\labelwidth-\labelsep}

%\setlength\lineskip{1\p@}
% \setlength\normallineskip{1\p@}
% \renewcommand\baselinestretch{}
% \setlength\parskip{0\p@ \@plus \p@}

% \setlength\textheight{676pt}%
\setlength\textheight{63\baselineskip}
%\addtolength\textheight{-2pt}%
%
%\setlength\normaltextheight{\textheight}%
\setlength\textwidth{500pt}%
%
%\setlength\typeheight{\textheight}%
%\setlength\typewidth{\textwidth}%
\hoffset-75pt
\voffset-66pt


\hbadness=10000
\vbadness=10000
\brokenpenalty=10000
\doublehyphendemerits=1000000
\finalhyphendemerits=1000000
\clubpenalty=10000
\widowpenalty=10000
\lefthyphenmin=3
\righthyphenmin=3
\uchyph=0



\setlength\topmargin{32pt}%
\setlength\oddsidemargin{52pt}%
\setlength\evensidemargin{52pt}%
%
\setlength\headheight{10\p@}%
\setlength\headsep   {42pt}% \typeheight - \textheight - \headheight
\setlength\topskip   {8\p@}
%
\setlength\footskip{40pt}
\setlength\maxdepth{48\baselineskip}
%
%\blindfoliodrop\trimheight
%\advance\blindfoliodrop-\typeheight
%\advance\blindfoliodrop-\topmargin
%\advance\blindfoliodrop-\footskip
%\advance\blindfoliodrop18pt
%
\setlength\parindent{18\p@}
%
\setlength\marginparwidth {.75in}
\setlength\marginparsep{22\p@}
\setlength\marginparpush{5\p@}
%
\setlength\footnotesep{\z@}
\setlength{\skip\footins}{17\p@}% \@plus 8\p@ \@minus 8\p@}% change + based on FN font height
\skip\@mpfootins = \skip\footins
%
\setlength\floatsep    {18\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\textfloatsep{24\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\intextsep   {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dblfloatsep    {12\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dbltextfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\@fptop{0\p@}
\setlength\@fpsep{8\p@ \@plus 1fil}
\setlength\@fpbot{0\p@ \@plus 1fil}
\setlength\@dblfptop{0\p@}
\setlength\@dblfpsep{8\p@ \@plus 1fil}
\setlength\@dblfpbot{0\p@ \@plus 1fil}
%
\setlength\partopsep{0pt}
\setlength\lineskip{1\p@}% check if it can be flexible
\setlength\normallineskip{1\p@}%
\renewcommand\baselinestretch{}
\setlength\parskip{\z@}%{0\p@ \@plus \p@}

\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301

\setcounter{topnumber}{2}
\renewcommand\topfraction{.7}
\setcounter{bottomnumber}{1}
\renewcommand\bottomfraction{.3}
\setcounter{totalnumber}{3}
\renewcommand\textfraction{.2}
\renewcommand\floatpagefraction{.5}
\setcounter{dbltopnumber}{2}
\renewcommand\dbltopfraction{.7}
\renewcommand\dblfloatpagefraction{.5}
% \if@twoside
  \def\ps@headings{%
      \def\@oddfoot{{\fontsize{10}{10}\selectfont\hfill\thepage}}
      \def\@evenfoot{{\fontsize{10}{10}\selectfont\thepage\hfill}}
      \def\@evenhead{\hbox to \textwidth{\raisebox{6pt}{{\fontfamily{\sfdefault}\fontseries{b}\fontsize{10}{10}\itshape\selectfont\raggedright\@journalname}{\fontfamily{\sfdefault}\fontsize{10}{10}\selectfont{\enspace\enspace}Vol.\@vol,{\enspace}Iss.~\@issue{\enspace}\the\year}\hfill}}\llap{\hspace*{10pt}\raisebox{-10pt}{\vrule width 520pt height 1pt depth0pt}\hspace*{-10pt}}}%
      \def\@oddhead{\hbox to \textwidth{\raisebox{6pt}{{\fontfamily{\sfdefault}\fontseries{b}\fontsize{10}{10}\itshape\selectfont\raggedright\@journalname}{\fontfamily{\sfdefault}\fontsize{10}{10}\selectfont{\enspace\enspace}Vol.\@vol,{\enspace}Iss.~\@issue{\enspace}\the\year}\hfill}}\llap{\hspace*{10pt}\raisebox{-10pt}{\vrule width 520pt height 1pt depth0pt}\hspace*{-10pt}}}%
      \let\@mkboth\markboth
    \def\sectionmark##1{%
      \markboth {\MakeUppercase{%
        \ifnum \c@secnumdepth >\z@
          \thesection\quad
        \fi
        ##1}}{}}%
    \def\subsectionmark##1{%
      \markright {%
        \ifnum \c@secnumdepth >\@ne
          \thesubsection\quad
        \fi
        ##1}}}
% \else
%   \def\ps@headings{%
%     \let\@oddfoot\@empty
%     \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
%     \let\@mkboth\markboth
%     \def\sectionmark##1{%
%       \markright {\MakeUppercase{%
%         \ifnum \c@secnumdepth >\m@ne
%           \thesection\quad
%         \fi
%         ##1}}}}
% \fi
\def\ps@myheadings{%
    \let\@oddfoot\@empty\let\@evenfoot\@empty
    \def\@evenhead{\thepage\hfil\slshape\leftmark}%
    \def\@oddhead{{\slshape\rightmark}\hfil\thepage}%
    \let\@mkboth\@gobbletwo
    \let\sectionmark\@gobble
    \let\subsectionmark\@gobble
    }


%
%
%\def\ausepspace{\hskip3pt}
%
%\def\auand{\comma\nobreakspace{}}%
%\def\aurunand{\comma}%
%\def\aubetweenand{{\fontsize{8.5}{14}\selectfont\uppercase{and}}}
%\def\aulastand{and}%
%\def\auandname{{\fontsize{8.5}{14}\selectfont\uppercase{and}}}%
%
% \def\author#1{%
%    \gdef\au@data{yes}%
%    \expandafter\protected@xdef\csname author\the\authorcount\endcsname{#1}%
%    \global\advance\authorcount1}
% %
% \def\andlastauname{%
% %\ifx\@auandbreak\undefined\else\@auandbreak\fi\gdef\AUxrefpresence{no}\unskip\unskip
% %\aulastand{}\ausepspace\null
% \csname author\the\tempcount\endcsname%\ifx\orcidau\YES\ifNOorcidrh\orcidbeforespace\null\orcid{}\else\fi\fi\unskip
% }
% %
% \gdef\@author{%
% %\begin{multicols}{3}
% %\multiaufalse
% %\global\augrouptrue
%    \global\tempauthorcount\authorcount%
%    \global\advance\tempauthorcount-1%
%    \global\authorcommacount\tempauthorcount%
%    \global\advance\authorcommacount-1%
%    \global\authortempcount0%
%    \global\authortempcount0%
% %   \ifnum\authorcount=1%
% %   \gdef\AUxrefpresence{no}
% %      \ignorespaces\csname author0\endcsname%\ifNOorcidrh\orcidbeforespace\orcid{}\else\fi%
% %   \else%
% %      \ifnum\authorcount=2%
% %      \gdef\AUxrefpresence{no}
% %         \ignorespaces\csname author0\endcsname\ifNOorcidrh\orcidbeforespace\orcid{}\else\fi\gdef\@givenname{}\ausepspace\null\aubetweenand\ausepspace\null\gdef\AUxrefpresence{no}\gdef\@ausuffix{}\csname author1\endcsname%\ifNOorcidrh\orcidbeforespace\orcid{}\else\fi%
% % %\if@twoauthors\else\fi\auandname\csname author1\endcsname%
% %      \else%
%                \@whilenum\tempcount<\tempauthorcount%
%    			       \do{%\vskip8pt
% %                     \gdef\AUxrefpresence{no}%
% %                     \ifx\orcidau\YES\gdef\orcidau{no}\else\fi%
% %                     \gdef\@ausuffix{}%
% %                     \multiautrue%
% % %              		 \csname author\the\tempcount\endcsname\unskip\unskip\comma\,\ \ifx\orcidau\YES\ifNOorcidrh\orcid{}\ \null\else \fi\else\fi\unskip\unskip%\space
%               		 \csname author\the\tempcount\endcsname%\unskip\unskip\ifx\orcidau\YES\ifNOorcidrh\orcidbeforespace\orcid{}\ausepspace\null\else\ausepspace\null\fi\else\ausepspace\null\fi\unskip\unskip%\space
%                      \global\advance\tempcount1 %\gdef\@givenname{}
%                      }%
%                %\aulastand\csname author\the\tempcount\endcsname\unskip%
%         %\ifx\orcidau\YES\gdef\orcidau{no}\else\fi%
%         %\multiaufalse
%         %\gdef\@ausuffix{}%
% 		%\ausepspace
% \andlastauname%
% %               \fi%
% % \global\augroupfalse%
% %           \fi
% %\end{multicols}
%            }

\def\affil#1{%
    \expandafter\protected@xdef\csname affil\the\affilcount\endcsname{#1}%
    \global\advance\affilcount1}%

\def\printaffil{\vspace*{-2.5pt}%
     \global\tempaffilcount\affilcount%
     \global\affiltempcount0%
     \global\advance\tempaffilcount-1
     \ifnum\affilcount=1%
     \ignorespaces\csname affil0\endcsname%
%     \protected@write\@auxout{}{\string\noaffnum}%
     \else%
     %\textcolor{red}{\the\tempaffilcount;\the\affiltempcount}
     \@whilenum\affiltempcount<\tempaffilcount%
     \do{\global\advance\afflabcnt1%\raisebox{2.5pt}
                \textsuperscript{\the\afflabcnt\kern1.5pt}\csname affil\the\affiltempcount\endcsname\vspace*{2pt}\@@par%
                \global\advance\affiltempcount1}%
                \global\advance\afflabcnt1%\raisebox{2.5pt}
                \textsuperscript{\the\afflabcnt\kern1.5pt}\csname affil\the\affiltempcount\endcsname\@@par\fi}%



\def\receivedname{Received:\ }
\def\revisedname{Revised:\ }
\def\acceptedname{Accepted:\ }
\def\publishedname{Published Online:\ }
\def\historysep{\hskip4.5pt{\raisebox{-2.5pt}{\rule{0.4pt}{10pt}}}\hskip4.5pt}
%\def\titlebarvoldatesep{\hskip4.75pt\textcolor{titlebarsep}{|}\hskip4.75pt}

\def\arttype#1{\gdef\@arttype{\uppercase{#1}}}\arttype{}
\def\received#1{\gdef\@received{#1}}\received{}
\def\revised#1{\gdef\@revised{#1}}\revised{}
\def\accepted#1{\gdef\@accepted{#1}}\accepted{}
\def\published#1{\gdef\@published{#1}}\published{}

\def\vol#1{\gdef\@vol{#1}}\vol{XX}
\def\issue#1{\gdef\@issue{#1}}\issue{XX}
\def\firstpage#1{\gdef\@firstpage{#1}}\firstpage{1}
\def\doi#1{\gdef\@doi{DOI: #1}}\doi{}
\def\OAText#1{\gdef\@OAText{#1}}\OAText{}

\gdef\@historyline{\hbox to \textwidth{\hfill\historyfont{{\receivedname}}\@received{\historysep}{{\revisedname}}\@revised{\historysep}{{\acceptedname}}\@accepted{\historysep}{{\publishedname}}\@published\hfill}}



\def\ps@plain{\let\@mkboth\@gobbletwo
     \let\@oddhead\@empty%
     \def\@oddfoot{\reset@font\hfill\thepage}%
     \let\@evenhead\@empty
%     \let\@evenfoot\@oddfoot%
     \def\@evenfoot{\reset@font\thepage
     \hfill}%
}

\def\ps@myplain{\let\@mkboth\@gobbletwo
     \def\@oddhead{\raisebox{-4pt}{\@historyline}}%
     \def\@evenhead{\raisebox{-4pt}{\@historyline}}
     \def\@oddfoot{\vbox to 24pt{%{\doifont{\ifdefvoid{\@doi}{}{https://doi.org/\@doi}}}\vspace*{-1em}\par
  \noindent\hbox to \textwidth{\parbox{400pt}{\doifont{\@OAText}\par}}}%
     {\fontsize{10}{10}\selectfont\hfill\thepage}}%
     \def\@evenfoot{{\fontsize{10}{10}\selectfont\thepage\hfill}}%
}


% \newenvironment{AUgroup}{\begingroup%
% \hsize\textwidth
% \begin{multicols}{3}
% }
% {\end{multicols}\endgroup}



% \if@titlepage
%   \newcommand\maketitle{\begin{titlepage}%
%   \let\footnotesize\small
%   \let\footnoterule\relax
%   \let \footnote \thanks
%   \null\vfil
%   \vskip 60\p@
%   \begin{center}%
%     {\titlefont\@title \par}%
%     \vskip 3em%
%     {\large
%      \lineskip .75em%
%       \begin{tabular}[t]{c}%
%         \@author
%       \end{tabular}\par}%
%       \vskip 1.5em%
%     {\large \@date \par}%       % Set date in \large size.
%   \end{center}\par
%   \@thanks
%   \vfil\null
%   \end{titlepage}%
%   \setcounter{footnote}{0}%
%   \global\let\thanks\relax
%   \global\let\maketitle\relax
%   \global\let\@thanks\@empty
%   \global\let\@author\@empty
%   \global\let\@date\@empty
%   \global\let\@title\@empty
%   \global\let\title\relax
%   \global\let\author\relax
%   \global\let\date\relax
%   \global\let\and\relax
%   }
% \else
%   \newcommand\maketitle{\par
%     \begingroup
%       \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
%       \def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
%       \long\def\@makefntext##1{\parindent 1em\noindent
%               \hb@xt@1.8em{%
%                 \hss\@textsuperscript{\normalfont\@thefnmark}}##1}%
%       \if@twocolumn
%         \ifnum \col@number=\@ne
%           \@maketitle
%         \else
%           \twocolumn[\@maketitle]%
%         \fi
%       \else
%       \newpage
%         \global\@topnum\z@   % Prevents figures from going at top of page.
%         \@maketitle
%       \fi
%       \thispagestyle{myplain}\@thanks
%     \endgroup
%     \setcounter{footnote}{0}%
%     \global\let\thanks\relax
%     \global\let\maketitle\relax
%     \global\let\@maketitle\relax
%     \global\let\@thanks\@empty
%     \global\let\@author\@empty
%     \global\let\@date\@empty
%     \global\let\@title\@empty
%     \global\let\title\relax
%     \global\let\author\relax
%     \global\let\date\relax
%     \global\let\and\relax
%   }
% \def\@maketitle{%
% %  \newpage
% %  \null
%   \vskip -3em%
% %  \begin{center}%
%   \let \footnote \thanks
%     {\titlefont\@title \par}%
%     \vskip 1.5em%
%     {\large
%       \lineskip .5em%
%         \authorfont\@author
%     \par}%
%     \vskip 1em%
% {%\ifx\@abstract\@undefined\else
% \abstractfont\unvbox\abstractbox{\par}\vskip7.5pt%\fi
% }%
% %    {\large \@date}%
% %  \end{center}%
%   \par
%   \vskip 1.5em}
% \fi
\setcounter{secnumdepth}{3}
\newcounter {part}
\newcounter {section}
\newcounter {subsection}[section]
\newcounter {subsubsection}[subsection]
\newcounter {paragraph}[subsubsection]
\newcounter {subparagraph}[paragraph]
\renewcommand \thepart {\@Roman\c@part}
\renewcommand \thesection {\@arabic\c@section}
\renewcommand\thesubsection   {\thesection.\@arabic\c@subsection}
\renewcommand\thesubsubsection{\thesubsection.\@arabic\c@subsubsection}
\renewcommand\theparagraph    {\thesubsubsection.\@arabic\c@paragraph}
\renewcommand\thesubparagraph {\theparagraph.\@arabic\c@subparagraph}
\newcommand\part{%
   \if@noskipsec \leavevmode \fi
   \par
   \addvspace{4ex}%
   \@afterindenttrue
   \secdef\@part\@spart}


\newcommand\section{\@startsection{section}{1}{\z@}{18pt plus1pt minus1pt}{6pt}{\sectionfont}}%
\newcommand\subsection{\@startsection{subsection}{2}{\z@}{15pt plus1pt minus1pt}{6pt}{\subsectionfont}}%
\newcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}{22pt plus1pt minus1pt}{6pt}{\subsubsectionfont}}%
\newcommand\paragraph{\@startsection{paragraph}{4}{\z@}{-2pt \@plus -2pt \@minus -.2pt}{-1.5pt}{\paragraphfont}}%
\newcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}{-19pt \@plus -2pt \@minus -.2pt}{0pt}{\subparagraphfont}}%
\newcommand\subsubparagraph{\@startsection{subsubparagraph}{6}{\parindent}{-19pt \@plus -2pt \@minus -.2pt}{-1em}{\subsubparagraphfont}}%
%
\newcommand\referencehead{\@startsection {section}{1}{\z@}{-24pt \@plus -2pt \@minus -.2pt}{2pt}{\referenceheadfont}}%
\newcommand\acknohead{\@startsection {section}{1}{\z@}{-24pt \@plus -2pt \@minus -.2pt}{6pt}{\acknoheadfont}}%

\def\@seccntformat#1{\csname the#1\endcsname.}

% \def\@sect#1#2#3#4#5#6[#7]#8{%\Abstractfalse%
%   \ifnum #2>\c@secnumdepth
%     \let\@svsec\@empty
%   \else
%     \refstepcounter{#1}%
%         \protected@edef\@svsec{\@seccntformat{#1}\hspace*{3.25pt}\relax}% \ifnum#2=1.\hspace*{3.25pt}\else\fi
%   \fi
%   \@tempskipa #5\relax
%   \ifdim \@tempskipa>\z@
%     \begingroup
%       #6{%
%          \ifnum#2=1%
%          %\def\spreadoutfactor{-.6}%
%          \@hangfrom{\hskip #3\relax\@svsec}% \ifappendix Appendix \@svsec\else\fi
%          \interlinepenalty \@M #8\@@par%
%          \else%
%          \ifnum#2=2%
%          \@hangfrom{\hskip #3\relax\@svsec}%
%          \interlinepenalty \@M #8\@@par%
%          %\ifonline\refstepcounter{HLsubsection}\pdfbookmark[2]{#8}{subsection.\theHLsubsection}\else\fi
%          \else
%          \ifnum#2=3%
%                   \@hangfrom{\hskip #3\relax\@svsec}%
%          \interlinepenalty \@M #8\@@par%
%          %\ifonline\refstepcounter{HLsubsubsection}\pdfbookmark[3]{#8}{subsubsection.\theHLsubsubsection}\else\fi
%          \else
%          \ifnum#2=4%
%                   \@hangfrom{\hskip #3\relax\@svsec}%
%          \interlinepenalty \@M #8\@@par%
%          \fi\fi\fi\fi}%
%     \endgroup
%     \csname #1mark\endcsname{#7}%
%     \addcontentsline{toc}{#1}{%
%       \ifnum #2>\c@secnumdepth \else
%         \protect\numberline{\csname the#1\endcsname}%
%       \fi
%       #7}%
%   \else
%     \def\@svsechd{%
%       #6{\hskip #3\relax%
%       \@svsec#8.\kern7pt}%
%       \csname #1mark\endcsname{#7}%
%       \addcontentsline{toc}{#1}{%
%         \ifnum #2>\c@secnumdepth \else
%           \protect\numberline{\csname the#1\endcsname}%
%         \fi
%         #7}}%
%   \fi
%   \@xsect{#5}}
%
\def\@ssect#1#2#3#4#5{%
  \@tempskipa #3\relax
  \ifdim \@tempskipa>\z@
%   \ifreview%
%     \begingroup
%       #4{%
%         \@hangfrom{\hskip #1}%
%           \interlinepenalty \@M {\reviewsym}{{#5}}\@@par}%
%     \endgroup
%   \else%
    \begingroup
      #4{%
        \@hangfrom{\hskip #1}%
          \interlinepenalty \@M {#5}\@@par}%
    \endgroup
%  \fi%
  \else
    \def\@svsechd{#4{\hskip #1\relax #5}}%
  \fi
  \@xsect{#3}}
%
\def\@startsection#1#2#3#4#5#6{%
  \if@noskipsec \leavevmode \fi
  \par
  \@tempskipa #4\relax
  \@afterindenttrue
  \ifdim \@tempskipa <\z@
    \@tempskipa -\@tempskipa
  \fi
  \if@nobreak
    \everypar{}%
  \else
    \addpenalty\@secpenalty\addvspace\@tempskipa
  \fi
  \@ifstar
    {\@ssect{#3}{#4}{#5}{#6}}%
    {\@dblarg{\@sect{#1}{#2}{#3}{#4}{#5}{#6}}}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  End Sectioning commands  %%%%%%%%%%%%%%%%


\def\maketitle{\par\thispagestyle{myplain}%%
  \begingroup%
  \parindent0pt%
    \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
    \def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
    \long\def\@makefntext##1{##1}%
     \twocolumn[\@maketitle]%
  \renewcommand\thefootnote{}%
%  \footnotetext{{\corresfont\printcorres\vskip0pt\ifx\@fund\undefined\else\@fund\fi\vskip0pt\ifx\@doi\undefined\else\@doi\fi}}%
%  \ifx\printcorres\undefined\else\footnotetext{\centerline{\corresfont\vbox to -3.5pt{\printcorres}}}\fi%
\@thanks
  \endgroup%
  \setcounter{footnote}{0}%
%  \enlargethispage{-17.5pt}%
% \advance\keywordcount0%
% \advance\authorcount0%
% \ifSingleColAbs
% {\ifx\@abstract\@undefined\else\abstractfont\noindent\ignorespaces\@abstract{\par}\vskip5.5pt\fi}%
% {\noindent\ifnum\c@keytext>0
% \noindent\printkeyword\ifnum\c@keytext=2\vskip7.5pt%
% \printkeyiiword\else\fi\else \vskip-7.5pt\fi}
%%%%% {\ifx\@abstract\@undefined\global\metadoitrue\else
%%%%% {\ifOAarticle%
%%%%%      %\def\LDcopyline{\relax}
%%%%%      \vskip6pt
%%%%%      {%\fontfamily{\sfdefault}\fontseries{m}\fontsize{8}{12}\selectfont\@copyline\par
%%%%%      \ifx\@doi\undefined\else\noindent\fontfamily{\sfdefault}\fontseries{m}\fontsize{8}{12}\selectfont%
%%%%% 	\ifonline%
%%%%% 	    \noindent{\textcolor{linkcolor}{\href{https://doi.org/\@doi}{https://doi.org/\@doi}}\par}%
%%%%% 	\else%
%%%%% 	    \noindent{https://doi.org/\@doi\par}%
%%%%% 	\fi%
%%%%%      	\vspace*{-3pt}\par
%%%%%      \fi}
%%%%% \else%
%%%%%      {\ifx\@doi\undefined\else\vskip6pt\fontfamily{\sfdefault}\fontseries{m}\fontsize{8}{12}\selectfont%
%%%%%      \ifonline%
%%%%% 	\noindent\textcolor{linkcolor}{\href{https://doi.org/\@doi}{https://doi.org/\@doi}}\par%
%%%%%      \else%
%%%%% 	\noindent{https://doi.org/\@doi\par}%
%%%%%      \fi%
%%%%%      \vspace*{-3pt}\par
%%%%%      \fi}
%%%%% \fi}
%%%%% \fi}
% \ifx\@abstract\@undefined\else\noindent\vrule width\columnwidth height0.4pt\par\fi
%\@afterindentfalse%%
\vskip9.5pt
%\enlargethispage{-24pt}
}


% \def\@part[#1]#2{%
%     \ifnum \c@secnumdepth >\m@ne
%       \refstepcounter{part}%
%       \addcontentsline{toc}{part}{\thepart\hspace{1em}#1}%
%     \else
%       \addcontentsline{toc}{part}{#1}%
%     \fi
%     {\parindent \z@ \raggedright
%      \interlinepenalty \@M
%      \normalfont
%      \ifnum \c@secnumdepth >\m@ne
%        \Large\bfseries \partname\nobreakspace\thepart
%        \par\nobreak
%      \fi
%      \huge \bfseries #2%
%      \markboth{}{}\par}%
%     \nobreak
%     \vskip 3ex
%     \@afterheading}
% \def\@spart#1{%
%     {\parindent \z@ \raggedright
%      \interlinepenalty \@M
%      \normalfont
%      \huge \bfseries #1\par}%
%      \nobreak
%      \vskip 3ex
%      \@afterheading}

% \newenvironment{keywords}{\par\noindent%
% \kwdfont{\keywordsname}\ }
% {\par}

  \newenvironment{keywords}{%
\global\setbox\keywordsbox\vbox
  \bgroup\vskip4.5pt\kwdfont%
\setlength\parindent{0pt}{\bfseries\keywordsname}:} %\  \par%
      {\egroup}

% \newenvironment{abstract}{%
%    \global\setbox\abstractbox\vbox%
%    \bgroup\abstractfont%
%    \setlength\parindent{0pt}}
%    {\par
% %   \vspace*{7pt}\ifx\@OCIScodes\@empty\else{{\bfseries {\OCISname}: }{\reset@font\kwdfont\@OCIScodes}}\fi\ifx\@doi\@empty\else\par{\bfseries DOI: }\reset@font\kwdfont\@doi\fi\egroup
%    }
% \ifx\@keywords\@empty\else{{\bfseries {\keywordname}: }{\reset@font\kwdfont\@keywords}}\fi


\def\journalname#1{\gdef\@journalname{#1}}
% \ifAAES%
%     \journalname{Archives of Advanced Engineering Science}%
% \else
%     \ifMEDIN
%         \journalname{Medinformatics}%
%     \else
%         \ifAIA%
            \journalname{Artificial Intelligence and Applications}%
%         \else
%             \ifGLCE%
%                 \journalname{Green and Low-Carbon Economy}%
%             \else
%                 \ifIJCE%
%                     \journalname{International Journal of Changes in Education}%
%                 \else
%                     \ifJCBAR%
%                         \journalname{Journal of Comprehensive Business Administration Research}%
%                     \else
%                         \ifJCCE%
%                             \journalname{Journal of Computational and Cognitive Engineering}%
%                         \else
%                             \ifJDSIS%
                                 % \journalname{Journal of Data Science and Intelligent Systems}%
%                             \else
%                                 \ifJOPR%
%                                     \journalname{Journal of Optics and Photonics Research}%
%                                 \else%
% %                                    \errmessage{Include the appropriate Journal-ID as a class option in the TeX file!!!}
%                                      \@latex@warning{Include the appropriate Journal-ID as a class option in the TeX file (for e.g. \protect\documentclass[JDSIS,authoryear]{BVP_MS-NEW})}
%                                      \journalname{\textcolor{red}{Journal Name}}%
%                                 \fi%
%                             \fi%
%                         \fi%
%                     \fi%
%                 \fi%
%             \fi%
%         \fi%
%     \fi%
% \fi%

\newenvironment{abstract}{%
   \global\setbox\abstractbox\vbox
   \bgroup\vskip4.5pt\abstractfont
   \setlength\parindent{0pt}{\bfseries\abstractname}:}%\leftskip9pt\rightskip9pt}
   {\egroup}

\def\@maketitle{\par%
{\parindent\z@%
\vspace*{-17.1pt}
{\begin{tabular*}{\textwidth}{@{\extracolsep{\fill}}p{300pt}r@{}}
\vbox to 73pt{{\arttypefont\@arttype\par}\vfill\titlefont\@title\par}
&
\begin{minipage}[t]{185pt}\fontsize{8}{10}\selectfont
\vspace*{-63pt}
\begin{flushright}\par
\vspace*{-1.4em}
{\@journalname}\\[1pt]
\the\year, Vol. \@vol(\@issue) \@firstpage--\pageref{lastpage}\\[1pt]
\ifx\@doi\undefined\else\@doi\fi\\[4pt]
\includegraphics[width=54pt]{logo/BVP-logo.pdf}
\end{flushright}
\end{minipage}\\[-4pt]
\noindent{\vrule width \textwidth height 0.5pt depth 0pt}\par\vskip-5pt
\end{tabular*}}
{{\authorfont\@author\par}}\vskip1.1em%
%{{\affilfont\@affil\par}}%
{\ifx\printaffil\undefined\else\affilfont\printaffil\fi%\printmember
\@par}\vskip1.3em%
\noindent{\vrule width \textwidth height 0.5pt depth 0pt}\par\vskip6pt
% {\ifx\printcorresp\undefined\else\correspfont\printcorresp\fi%\printmember
% }%
%{\@historyline\par}%
{%\ifx\@abstract\@undefined\else
{\abstractfont\unvbox\abstractbox{\par}}\vskip6pt%\fi
}%
{%\ifx\@abstract\@undefined\else
{\kwdfont\unvbox\keywordsbox{\par}}\vspace*{-3pt}%\fi
}%
\noindent{\vrule width \textwidth height 0.5pt depth 0pt}\par
%{\ifx\@corid\undefined\else\vskip-1.5pt{{\corresfont \unhbox\correspbox}}\fi\vskip8pt}%
%{\ifx\printhistory\undefined\else\printhistory\par\vskip1pt\fi}%
%
%     \ifx\@abstract\@undefined\vskip10pt\par\else\ifnum\c@keytext>0\else\vskip3pt\fi\fi%
}
%\vskip29pt%
% \ifSingleColAbs\addvspace{14pt}\else\addvspace{29pt}\fi%
\addvspace{20pt}
% \vspace*{\mktitleskip}%
%\@afterheading%
\@afterindenttrue%
\setcounter{section}{0}
}




\def\@seccntformat#1{\csname the#1\endcsname.}

\def\@sect#1#2#3#4#5#6[#7]#8{%\Abstractfalse%
  \ifnum #2>\c@secnumdepth
    \let\@svsec\@empty
  \else
    \refstepcounter{#1}%
        \protected@edef\@svsec{\@seccntformat{#1}\hspace*{6pt}\relax}% \ifnum#2=1.\hspace*{3.25pt}\else\fi
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
    \begingroup
      #6{%
         \ifnum#2=1%
         %\def\spreadoutfactor{-.6}%
         \@hangfrom{\hskip #3\relax{\@svsec}}% \ifappendix Appendix \@svsec\else\fi
         \interlinepenalty \@M {#8}\@@par%
         \else%
         \ifnum#2=2%
         \@hangfrom{\hskip #3\relax{\@svsec}}%
         \interlinepenalty \@M {#8}\@@par%
         %\ifonline\refstepcounter{HLsubsection}\pdfbookmark[2]{#8}{subsection.\theHLsubsection}\else\fi
         \else
         \ifnum#2=3%
                  \@hangfrom{\hskip #3\relax{\@svsec}}%
         \interlinepenalty \@M {#8}\@@par%
         %\ifonline\refstepcounter{HLsubsubsection}\pdfbookmark[3]{#8}{subsubsection.\theHLsubsubsection}\else\fi
         \else
         \ifnum#2=4%
                  \@hangfrom{\hskip #3\relax{\@svsec}}%
         \interlinepenalty \@M {#8}\@@par%
         \fi\fi\fi\fi}%
    \endgroup
    \csname #1mark\endcsname{#7}%
    \addcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      #7}%
  \else
    \def\@svsechd{%
      #6{\hskip #3\relax%
      \@svsec#8.\kern7pt}%
      \csname #1mark\endcsname{#7}%
      \addcontentsline{toc}{#1}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        #7}}%
  \fi
  \@xsect{#5}}
%
% \def\@ssect#1#2#3#4#5{%
%   \@tempskipa #3\relax
%   \ifdim \@tempskipa>\z@
% %   \ifreview%
% %     \begingroup
% %       #4{%
% %         \@hangfrom{\hskip #1}%
% %           \interlinepenalty \@M {\reviewsym}{{#5}}\@@par}%
% %     \endgroup
% %   \else%
%     \begingroup
%       #4{%
%         %\@hangfrom
%         {\hskip #1}%
%           \interlinepenalty \@M {{#5}}\@@par}%
%     \endgroup
% %  \fi%
%   \else
%     \def\@svsechd{#4{\hskip #1\relax #5}}%
%   \fi
%   \@xsect{#3}}
%
% \def\@startsection#1#2#3#4#5#6{%
%   \if@noskipsec \leavevmode \fi
%   \par
%   \@tempskipa #4\relax
%   \@afterindenttrue
%   \ifdim \@tempskipa <\z@
%     \@tempskipa -\@tempskipa
%   \fi
%   \if@nobreak
%     \everypar{}%
%   \else
%     \addpenalty\@secpenalty\addvspace\@tempskipa
%   \fi
%   \@ifstar
%     {\@ssect{#3}{#4}{#5}{#6}}%
%     {\@dblarg{\@sect{#1}{#2}{#3}{#4}{#5}{#6}}}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  End Sectioning commands  %%%%%%%%%%%%%%%%



% \newcommand\section{\@startsection {section}{1}{\z@}%
%                                    {-3ex \@plus -1ex \@minus -.2ex}%
%                                    {1.8ex}%
%                                    {\sectionfont}}
% \newcommand\subsection{\@startsection{subsection}{2}{\z@}%
%                                      {-2.25ex\@plus -1ex \@minus -.2ex}%
%                                      {1.5ex \@plus .2ex}%
%                                      {\subsectionfont}}
% \newcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
%                                      {-3.25ex\@plus -1ex \@minus -.2ex}%
%                                      {1.5ex \@plus .2ex}%
%                                      {\subsubsectionfont}}
% \newcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
%                                     {3.25ex \@plus1ex \@minus.2ex}%
%                                     {-0.01em}%
%                                     {\paragraphfont}}
% \newcommand\subparagraph{\@startsection{subparagraph}{5}{\parindent}%
%                                        {3.25ex \@plus1ex \@minus .2ex}%
%                                        {-1em}%
%                                       {\subparagraphfont}}
\if@twocolumn
  \setlength\leftmargini  {2em}
\else
  \setlength\leftmargini  {2.5em}
\fi
\leftmargin  \leftmargini
\setlength\leftmarginii  {2.2em}
\setlength\leftmarginiii {1.87em}
\setlength\leftmarginiv  {1.7em}
\if@twocolumn
  \setlength\leftmarginv  {.5em}
  \setlength\leftmarginvi {.5em}
\else
  \setlength\leftmarginv  {1em}
  \setlength\leftmarginvi {1em}
\fi
\setlength  \labelsep  {.5em}
\setlength  \labelwidth{\leftmargini}
\addtolength\labelwidth{-\labelsep}
\@beginparpenalty -\@lowpenalty
\@endparpenalty   -\@lowpenalty
\@itempenalty     -\@lowpenalty
\renewcommand\theenumi{\@arabic\c@enumi}
\renewcommand\theenumii{\@alph\c@enumii}
\renewcommand\theenumiii{\@roman\c@enumiii}
\renewcommand\theenumiv{\@Alph\c@enumiv}
\newcommand\labelenumi{\theenumi.}
\newcommand\labelenumii{(\theenumii)}
\newcommand\labelenumiii{\theenumiii.}
\newcommand\labelenumiv{\theenumiv.}
\renewcommand\p@enumii{\theenumi}
\renewcommand\p@enumiii{\theenumi(\theenumii)}
\renewcommand\p@enumiv{\p@enumiii\theenumiii}
\newcommand\labelitemi  {\labelitemfont \textbullet}
\newcommand\labelitemii {\labelitemfont \bfseries \textendash}
\newcommand\labelitemiii{\labelitemfont \textasteriskcentered}
\newcommand\labelitemiv{ \labelitemfont \textperiodcentered}
\newcommand\labelitemfont{\normalfont}
\newenvironment{description}
               {\list{}{\labelwidth\z@ \itemindent-\leftmargin
                        \let\makelabel\descriptionlabel}}
               {\endlist}
\newcommand*\descriptionlabel[1]{\hspace\labelsep
                                \normalfont\bfseries #1}
% \if@titlepage
%   \newenvironment{abstract}{%
%       \titlepage
%       \null\vfil
%       \@beginparpenalty\@lowpenalty
%       \begin{center}%
%         \bfseries \abstractname
%         \@endparpenalty\@M
%       \end{center}}%
%      {\par\vfil\null\endtitlepage}
% \else
%   \newenvironment{abstract}{%
%       \if@twocolumn
%         \section*{\abstractname}%
%       \else
%         \small
%         \begin{center}%
%           {\bfseries \abstractname\vspace{-.5em}\vspace{\z@}}%
%         \end{center}%
%         \quotation
%       \fi}
%       {\if@twocolumn\else\endquotation\fi}
%   \newenvironment{abstract}{\noindent%\begingroup\par%
% \abstractfont{{\bfseries\abstractname:}}\ \ignorespaces%
%       }
%       {\endgroup}
%      {\if@twocolumn\else\endquotation\fi}
% \fi
\newenvironment{verse}
               {\let\\\@centercr
                \list{}{\itemsep      \z@
                        \itemindent   -1.5em%
                        \listparindent\itemindent
                        \rightmargin  \leftmargin
                        \advance\leftmargin 1.5em}%
                \item\relax}
               {\endlist}
\newenvironment{quotation}
               {\list{}{\listparindent 1.5em%
                        \itemindent    \listparindent
                        \rightmargin   \leftmargin
                        \parsep        \z@ \@plus\p@}%
                \item\relax}
               {\endlist}
\newenvironment{quote}
               {\list{}{\rightmargin\leftmargin}%
                \item\relax}
               {\endlist}


\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}
\newtheorem{proposition}{Proposition}

\theoremstyle{definition}
\newtheorem{definition}{Definition}
\newtheorem{example}{Example}

\theoremstyle{remark}
\newtheorem*{remark}{Remark}
%\newtheorem*{proof}{Proof}



% \if@compatibility
%   \newenvironment{titlepage}
%     {%
%       \if@twocolumn
%         \@restonecoltrue\onecolumn
%       \else
%         \@restonecolfalse\newpage
%       \fi
%       \thispagestyle{empty}%
%       \setcounter{page}\z@
%     }%
%     {\if@restonecol\twocolumn \else \newpage \fi
%     }
% \else
%   \newenvironment{titlepage}
%     {%
%       \if@twocolumn
%         \@restonecoltrue\onecolumn
%       \else
%         \@restonecolfalse\newpage
%       \fi
%       \thispagestyle{empty}%
%       \setcounter{page}\@ne
%     }%
%     {\if@restonecol\twocolumn \else \newpage \fi
%      \if@twoside\else
%         \setcounter{page}\@ne
%      \fi
%     }
% \fi
% \newcommand\appendix{\par
%   \setcounter{section}{0}%
%   \setcounter{subsection}{0}%
%   \gdef\thesection{\@Alph\c@section}}
% \setlength\arraycolsep{5\p@}
% \setlength\tabcolsep{6\p@}
% \setlength\arrayrulewidth{.4\p@}
% \setlength\doublerulesep{2\p@}
% \setlength\tabbingsep{\labelsep}
% \skip\@mpfootins = \skip\footins
% \setlength\fboxsep{3\p@}
% \setlength\fboxrule{.4\p@}
% \renewcommand \theequation {\@arabic\c@equation}
% \newcounter{figure}
% \newcommand \thefigure {\@arabic\c@figure}
% % \def\fps@figure{tbp}
% % \def\ftype@figure{1}
% % \def\ext@figure{lof}
% % \def\fnum@figure{\figurename\nobreakspace\thefigure}
% % \newenvironment{figure}
% %                {\@float{figure}}
% %                {\end@float}
% % \newenvironment{figure*}
% %                {\@dblfloat{figure}}
% %                {\end@dblfloat}
% \newcounter{table}
% \newcommand\thetable{\@arabic\c@table}
% % \def\fps@table{tbp}
% % \def\ftype@table{2}
% % \def\ext@table{lot}
% % \def\fnum@table{\tablename\nobreakspace\thetable}
% % \newenvironment{table}
% %                {\@float{table}}
% %                {\end@float}
% % \newenvironment{table*}
% %                {\@dblfloat{table}}
% %                {\end@dblfloat}
\newlength\abovecaptionskip
\newlength\belowcaptionskip
\setlength\abovecaptionskip{0\p@}
\setlength\belowcaptionskip{0\p@}

% \long\def\@makecaption#1#2{%
%   \vskip\abovecaptionskip
%   \sbox\@tempboxa{#1: #2}%
%   \ifdim \wd\@tempboxa >\hsize
%     #1: #2\par
%   \else
%     \global \@minipagefalse
%     \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
%   \fi
%   \vskip\belowcaptionskip}
\def\figcaptiondesc#1{\gdef\@figcaptiondesc{#1}}
\figcaptiondesc{}
%
\renewcommand\thefigure{\@arabic\c@figure}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}

% \def\figurehead#1{\gdef\@figurehead{#1}}\figurehead{}
\def\fnum@figure{\figcaptionnumfont{\figurename~\thefigure}}

\newif\ifimage\global\imagefalse

%\newenvironment{figure}
%               {\global\imagetrue\@float{figure}}
%               {\end@float\global\imagefalse\global\nosidecapfalse}

\newenvironment{figure}
               {\global\imagetrue\@float{figure}} %
               {\end@float\global\imagefalse} %\global\nosidecapfalse\global\swapfigfalse}

\def\@float#1{%
  \@ifnextchar[%
    {\@xfloat{#1}}%
    {\edef\reserved@a{\noexpand\@xfloat{#1}[\csname fps@#1\endcsname]}%
     \reserved@a}}
\newenvironment{figure*}
               {\@dblfloat{figure}}
               {\end@dblfloat}
%
\newenvironment{Figure}
               {\par\addvspace{12pt plus2pt}\def\@captype{figure}}
               {\par\addvspace{12pt plus2pt}}
%
\newenvironment{Figure*}
               {\par\addvspace{12pt plus2pt}\def\@captype{figure}}
               {\par\addvspace{12pt plus2pt}}

\def\figlabelfont{\fontsize{10}{12}\selectfont}
\def\figlabel#1{\gdef\@figlabel{#1}}
\figlabel{}
%
%\figcaptionleftskip0pt
%\figcaptionrightskip0pt
% \figindent0pt
% \figwidthcapdimen12pt
%\figleftskip0pt
%\figrightskip0pt
%\adjustskip0pt
%
\newdimen\figcappush
\newdimen\figcappull
\newbox\figscapbox

%\newif\ifnosidecap\global\nosidecapfalse

%\def\sidecapoff{\global\nosidecaptrue}

%\def\swapfig{\global\swapfigtrue}

\def\figpunct{.}

%%%%%%%figure sidecaption%%%%%%%%%%
\newbox\figbox
\newdimen\figheight%

\def\@makefigurecaption#1#2{\figcaptionfont%\raggedright%
\global\setbox\figcapbox\hbox{\figcaptionfont
{\figcaptiondescfont\@figcaptiondesc}\hskip\figcapdescsep#2}\par
% \ifMEDIN%
% \def\capprint{\centerline{\copy\figbox}{\figcaptionnumfont\fontseries{b}#1\figpunct}\hskip2.5pt{\unhbox\figcapbox}\vskip6pt}%
% \else%
%\def\capprint{\centerline{\copy\figbox}\centerline{\figcaptionnumfont\fontseries{b}#1}\par\centerline{\unhbox\figcapbox}\vskip6pt}%
\def\capprint{\centering{\copy\figbox}{\figcaptionnumfont\fontseries{b}#1\figpunct}\par{\unhbox\figcapbox}\vskip6pt}
% \fi%
% \ifnosidecap\capprint\else%
% \ifdim\wd\figbox<245pt%
% \figcappush\wd\figbox%
% \advance\figcappush12pt%
% \global\setbox\figscapbox\vbox{\ifodd\c@page\ifswapfig\leftskip\else\rightskip\fi\else\ifswapfig\rightskip\else\leftskip\fi\fi\figcappush\unhbox\figcapbox}%
% \def\placefig{\copy\figbox\vspace*{-\ht\figscapbox}\unvbox\figscapbox}
% \ifodd\c@page\ifswapfig\placefig\vspace*{\textfloatsep}\else\hfill\placefig\fi\else\ifswapfig\hfill\placefig\else\placefig\vspace*{\textfloatsep}\fi\fi%
% \else%
\capprint%
%\fi\fi
}


\def\FigName{figure}
% \def\TabName{table}
%
\long\def\@makecaption#1#2{%
    \ifx\FigName\@captype
      \@makefigurecaption{#1}{#2}%
%      \vskip0pt
      \vskip\belowcaptionskip
    \else
%     \ifx\TabName\@captype
      \@maketablecaption{#1}{#2}%
      \vskip\belowcaptionskip
%       \else
%       \fi
    \fi
    }


%\renewcommand\thetable{\Roman{table}}
%
\def\fps@table{tbp}
\def\ftype@table{2}
\def\ext@table{lot}
\def\fnum@table{\tablename\ \thetable\ }
%
\def\tablefootnote#1{
        \global\advance\tfootcount1\expandafter\gdef\csname tablefootnote\the\tfootcount\endcsname{#1}}
%
\newenvironment{table}
               {%\global\tableshowtrue
               \let\footnote\tablefootnote%
               \@float{table}}
               {\end@float\gdef\@tbnote{}} %\global\tableshowfalse
%
\def\tablebelowspace#1{\gdef\@tablebelowspace{#1}}\tablebelowspace{}
%
\newenvironment{table*}
               {\let\footnote\tablefootnote%%
               \@dblfloat{table}}
               {%
                  \ifx\@tablebelowspace\@empty%
                  \else%
                    \vspace*{\@tablebelowspace}\tablebelowspace{}%
                  \fi%
               \end@dblfloat}
%

\newenvironment{Table}
               {\par\addvspace{12pt plus2pt}\def\@captype{table}}
               {\par\addvspace{12pt plus2pt}}
%
\newenvironment{boxtextTable}[1][\relax]%
               {\par\addvspace{12pt plus2pt}\def\@captype{table}}
               {\par\addvspace{12pt plus2pt}}
%
\newenvironment{Table*}
               {\par\addvspace{12pt plus2pt}\def\@captype{table}}
               {\par\addvspace{12pt plus2pt}}
%
\def\tableabovespace#1{\gdef\@tableabovespace{#1}}\tableabovespace{}
%

\tablenumcapsep=1.25pt
\def\TCH#1{\TCHfont#1}
%
\def\tableshade#1{\gdef\@tableshade{#1}}\tableshade{0pt}%
\def\tableruleheight#1{\gdef\@tableruleheight{#1}}\tableruleheight{138pt}%
%
\def\tbnote#1{\gdef\@tbnote{#1\par}}\tbnote{}%

\long\def\multicolumn#1#2#3{\multispan{#1}\begingroup
  \@mkpream{#2}%
  \def\@sharp{#3}%\setbox\tempbox\hbox{#3}\raise-5pt\hbox to 0pt{\hfill\hbox{\vrule height.5pt width\wd\tempbox depth0pt}}
  \set@typeset@protect
  \let\@startpbox\@@startpbox\let\@endpbox\@@endpbox
  \@arstrut \@preamble\hbox{}\endgroup\ignorespaces}
%
\def\@cline#1-#2\@nil{%
  \omit
  \@multicnt#1%
  \advance\@multispan\m@ne
  \ifnum\@multicnt=\@ne\@firstofone{&\omit}\fi
  \@multicnt#2%
  \advance\@multicnt-#1%
  \advance\@multispan\@ne
  \leaders\hrule\@height\arrayrulewidth\hfill
  \cr
  \noalign{\vskip-\arrayrulewidth}}
%
%%%%%%%%%%%%%%% B-Table Rules %%%%%%%%%%%%%%
%%%%%%%%%%%%%%% B-Table Rules %%%%%%%%%%%%%%
%
\toprulewidth=0.5pt%.47pt
\midrulewidth=0.25pt%.47pt
\botrulewidth=\toprulewidth
\cmidrulewidth=0.25pt%.42pt
\belowbottomsep=0pt
\abovetopsep=0pt
\cmidrulesep=\doublerulesep
\cmidrulekern=.5em
\defaultaddspace=.5em
%
\newdimen\TableWidth%%
\newdimen\TableHeight%%
\newdimen\Tablecapht%%
\newdimen\spancolwidth%%
\newdimen\ccolumnwd%%
\newdimen\tempspancolwidth%%
\newdimen\tempaspancolwidth%%
\newdimen\addedcolsep%%
\newdimen\@@star@colcount%%%
\newdimen\@@TotalTableWidth%%
\newdimen\thatdim%%
\newdimen\thisdim%%
\newdimen\total@colsep%%
\newdimen\ext@colsep%%
\newdimen\tempadim%%
\newdimen\tabfirstcolsep%%
\newdimen\tabsecondcolsep%%
\newdimen\tablastcolsep%%
\newdimen\TB@dimen@one\TB@dimen@one10\p@%%
\newdimen\TB@dimen@two\TB@dimen@two40\p@%%

\newcount\tbodycount\tbodycount=0%%
\newcount\tempfltcount%%
\newcount\tqrtcount\tqrtcount=0%%
\newcount\ttqrtcount\ttqrtcount=0%%
\newcount\captionintab%%
\newcount\Ncols%%
\newcount\colcount%%
\newcount\rowcount%%
\newcount\spancolcount%%
\newcount\AlltgroupCount%%
\newcount\tabcount%%
\newcount\tabnotecount%%
\newcount\tempColnum%%
\newcount\colspancount%%
\newcount\starcolcount%%
\newcount\tempcounta%%
\newcount\col@cnta%%
\newcount\col@cnt%%
\newcount\col@cntc%%
\newcount\spanstart%%
\newcount\spanend%%
\newcount\chkcount%%
\newcount\temp@cnta%%
\newcount\temp@cntb%%
\newcount\temp@cntc\temp@cntc=0%%
\newcount\temp@cntd%%
\newcount\temp@cnte%%
\newcount\coltintpercent%%
\newcount\tqrtcount\tqrtcount0%
\newcount\ttqrtcount\ttqrtcount=0%
\newcount\TB@tempcount\TB@tempcount0%
\newcount\aidcount\aidcount0%
\newcount\colcount

%%%%%%%%%%%%%%% B-BookTabs %%%%%%%%%%%%%%
\newcount\@cmidla
\newcount\@cmidlb
\newdimen\@aboverulesep
\newdimen\@belowrulesep
\newcount\@thisruleclass
\newcount\@lastruleclass
%%%%%%%%%%%%%%% E-BookTabs %%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% B-Booktabs Materials %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
\@lastruleclass=0
\def\futurenonspacelet#1{\def\@BTcs{#1}%
   \afterassignment\@BTfnslone\let\nexttoken= }
\def\@BTfnslone{\expandafter\futurelet\@BTcs\@BTfnsltwo}
\def\@BTfnsltwo{\expandafter\ifx\@BTcs\@sptoken\let\next=\@BTfnslthree
   \else\let\next=\nexttoken\fi \next}
\def\@BTfnslthree{\afterassignment\@BTfnslone\let\next= }
\def\topline{\noalign{\ifnum0=`}\fi
  \@aboverulesep=\aboverulesep
  \global\@belowrulesep=\belowrulesep %global cos for use in the next noalign
  \global\@thisruleclass=\@ne
  \@ifnextchar[{\@BTrule}{\@BTrule[\toprulewidth]}}
\def\midline{\noalign{\ifnum0=`}\fi
  \@aboverulesep=\aboverulesep
  \global\@belowrulesep=\belowrulesep
  \global\@thisruleclass=\@ne
  \@ifnextchar[{\@BTrule}{\@BTrule[\midrulewidth]}}
\def\botline{\noalign{\ifnum0=`}\fi
  \@aboverulesep=\aboverulesep
  \global\@belowrulesep=\belowrulesep
  \global\@thisruleclass=\@ne
  \@ifnextchar[{\@BTrule}{\@BTrule[\botrulewidth]}}
\def\specialrule#1#2#3{\noalign{\ifnum0=`}\fi
  \@aboverulesep=#2\global\@belowrulesep=#3\global\@thisruleclass=\tw@
  \@BTrule[#1]}
\def\addlinespace{\noalign{\ifnum0=`}\fi
  \@ifnextchar[{\@addspace}{\@addspace[\defaultaddspace]}}
\def\@addspace[#1]{\global\@belowrulesep=#1\global\@thisruleclass=\tw@
  \futurelet\@tempa\@BTendrule}
\def\@BTrule[#1]{%
  \global\@thisrulewidth=#1\relax
  \ifnum\@thisruleclass=\tw@\vskip\@aboverulesep\else
  \ifnum\@lastruleclass=\z@\vskip\@aboverulesep\else
  \ifnum\@lastruleclass=\@ne\vskip\doublerulesep\fi\fi\fi
  \ifx\longtable\undefined
     \let\@BTswitch\@BTnormal
  \else\ifx\hline\LT@hline
     \let\@BTswitch\@BLTrule
  \else
     \let\@BTswitch\@BTnormal
  \fi\fi
  \@BTswitch}
\AtBeginDocument{%
   \providecommand*\CT@arc@{}}%% colortbl support
\def\@BTnormal{%\color{aucolor}{%
    {\CT@arc@\hrule\@height\@thisrulewidth}%
    \futurenonspacelet\@tempa\@BTendrule}%}
\def\@BLTrule{\@ifnextchar({\@@BLTrule}{\@@BLTrule()}}
\def\@@BLTrule(#1){\@setrulekerning{#1}%
\global\@cmidlb\LT@cols
\ifnum0=`{\fi}%
\@cmidruleb
\noalign{\ifnum0=`}\fi
\futurenonspacelet\@tempa\@BTendrule}
\def\@BTendrule{%
\ifx\@tempa\toprule\global\@lastruleclass=\@thisruleclass
\else
    \ifx\@tempa\midrule\global\@lastruleclass=\@thisruleclass
    \else
        \ifx\@tempa\bottomrule\global\@lastruleclass=\@thisruleclass
        \else
            \ifx\@tempa\cmidrule\global\@lastruleclass=\@thisruleclass
            \else
                \ifx\@tempa\specialrule\global\@lastruleclass=\@thisruleclass
                \else
                    \ifx\@tempa\addlinespace\global\@lastruleclass=\@thisruleclass
                    \else
                        \global\@lastruleclass=\z@
                    \fi
                \fi
            \fi
        \fi
    \fi
\fi
  \ifnum\@lastruleclass=\@ne\relax\else\vskip\@belowrulesep\fi
  \ifnum0=`{\fi}
  }
\def\@setrulekerning#1{%
   \global\let\cmrkern@l\z@
   \global\let\cmrkern@r\z@
   \@tfor\@tempa :=#1\do
  {\def\@tempb{r}%
   \ifx\@tempa\@tempb
      \global\let\cmrkern@r\cmidrulekern
      \def\cmrsideswitch{\cmrkern@r}%
   \else
      \def\@tempb{l}%
      \ifx\@tempa\@tempb
         \global\let\cmrkern@l\cmidrulekern
         \def\cmrsideswitch{\cmrkern@l}%
      \else
         \global\expandafter\let\cmrsideswitch\@tempa
      \fi
   \fi}}
\def\cmidrule{\noalign{\ifnum0=`}\fi
    \@ifnextchar[{\@cmidrule}{\@cmidrule[\cmidrulewidth]}}
\def\@cmidrule[#1]{\@ifnextchar({\@@cmidrule[#1]}{\@@cmidrule[#1]()}}
\def\@@cmidrule[#1](#2)#3{\@@@cmidrule[#3]{#1}{#2}}
\def\@@@cmidrule[#1-#2]#3#4{\global\@cmidla#1\relax
    \global\advance\@cmidla\m@ne
    \ifnum\@cmidla>0\global\let\@gtempa\@cmidrulea\else
    \global\let\@gtempa\@cmidruleb\fi
    \global\@cmidlb#2\relax
    \global\advance\@cmidlb-\@cmidla
    \global\@thisrulewidth=#3
    \@setrulekerning{#4}
    \ifnum\@lastruleclass=\z@\vskip \aboverulesep\fi
    \ifnum0=`{\fi}\@gtempa
    \noalign{\ifnum0=`}\fi\futurenonspacelet\@tempa\@xcmidrule}
\def\@xcmidrule{%
   \ifx\@tempa\cmidrule
       \vskip-\@thisrulewidth
       \global\@lastruleclass=\@ne
   \else \ifx\@tempa\morecmidrules
       \vskip \cmidrulesep
       \global\@lastruleclass=\@ne\else
       \vskip \belowrulesep
       \global\@lastruleclass=\z@
   \fi\fi
   \ifnum0=`{\fi}}
\def\@cmidrulea{%
   \multispan\@cmidla&\multispan\@cmidlb
   \unskip\hskip\cmrkern@l%
  {\CT@arc@\leaders\hrule \@height\@thisrulewidth\hfill}%
   \hskip\cmrkern@r\cr}%
\def\@cmidruleb{%
    \multispan\@cmidlb
    \unskip\hskip \cmrkern@l%
   {\CT@arc@\leaders\hrule \@height\@thisrulewidth\hfill}%
    \hskip\cmrkern@r\cr}%
\def\morecmidrules{\noalign{\relax}}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% E-Booktabs Materials %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\def\tabtoprule{\TOPrule}
\def\tabmidrule{\COLrule}
\def\tabbotrule{\BOTrule}


\tabfirstcolsep=0.5pc%%
\tabsecondcolsep=0.5pc%%
\tablastcolsep=\z@%


%%%%%%%%%%%%%%% E-Table Rules %%%%%%%%%%%%%%

\def\Hline{%
  \noalign{\ifnum0=`}\fi\hrule \@height .5pt \futurelet%\@height \arrayrulewidth
   \@tempa\@xhline}
%
\def\Mline{%
  \noalign{\ifnum0=`}\fi\hrule \@height 0pt \futurelet%\@height \arrayrulewidth
   \@tempa\@xhline}
%
\def\topline{%
  \noalign{\ifnum0=`}\fi\hrule \@height .5pt \futurelet%\@height \arrayrulewidth
   \@tempa\@xhline}

% \def\colline{%
%   \noalign{\ifnum0=`}\fi\hrule \@height .25pt \futurelet%\@height \arrayrulewidth
%    \@tempa\@xhline}


\def\toprule{\\[-8.5pt]\topline\\[-8.5pt]}
\def\midrule{\\[-8.5pt]\midline\\[-6pt]}
\def\botrule{\\[-9.5pt]\botline\\[-8pt]}
%


\def\@maketablecaption#1#2{
% \setbox\tabcapbox\vbox{{\centering\tablecaptionfont{\tablecaptionnumfont#1}\par
% {\centering #2.\vphantom{y}}\par\vskip.8pt}}
%\ifdim\wd\tabcapbox<\textwidth
%\ifdim\ht\tabcapbox<19pt
%\centerlast
% \ifMEDIN%
% {\tablecaptionfont{\tablecaptionnumfont#1\figpunct}\hskip2.5pt{#2\vphantom{y}}\par}%\global\unnumtablefalse%
% \else%
{\centering\tablecaptionfont{\tablecaptionnumfont#1}\par
{\centering #2\vphantom{y}}\par}%\global\unnumtablefalse%
% \fi%
% \else
% {\tablecaptionfont\noindent{\tablecaptionnumfont#1}{\tablecaptionnumfont}\hskip\tablenumcapsep#2.\vphantom{y}\vskip.8pt}%\global\unnumtablefalse%
% \fi
}


\def\enddocument{\label{lastpage}%
   \@kernel@before@enddocument
   \UseOneTimeHook{enddocument}%
   \@kernel@after@enddocument
   \@checkend{document}%
   \clearpage
   \UseOneTimeHook{enddocument/afterlastpage}%
   \@kernel@after@enddocument@afterlastpage
   \begingroup
     \if@filesw
       \immediate\closeout\@mainaux
       \let\@setckpt\@gobbletwo
       \let\@newl@bel\@testdef
       \@tempswafalse
       \makeatletter \@@input\jobname.aux
     \fi
     \UseOneTimeHook{enddocument/afteraux}%
     \UseOneTimeHook{enddocument/info}%
   \endgroup
   \UseOneTimeHook{enddocument/end}%
   \deadcycles\z@\@@end}


\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}
\DeclareRobustCommand*\cal{\@fontswitch\relax\mathcal}
\DeclareRobustCommand*\mit{\@fontswitch\relax\mathnormal}
\newcommand\@pnumwidth{1.55em}
\newcommand\@tocrmarg{2.55em}
\newcommand\@dotsep{4.5}
\setcounter{tocdepth}{3}
\newcommand\tableofcontents{%
    \section*{\contentsname
        \@mkboth{%
           \MakeUppercase\contentsname}{\MakeUppercase\contentsname}}%
    \@starttoc{toc}%
    }
\newcommand*\l@part[2]{%
  \ifnum \c@tocdepth >-2\relax
    \addpenalty\@secpenalty
    \addvspace{2.25em \@plus\p@}%
    \setlength\@tempdima{3em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      {\leavevmode
       \large \bfseries #1\hfil
       \hb@xt@\@pnumwidth{\hss #2%
                          \kern-\p@\kern\p@}}\par
       \nobreak
       \if@compatibility
         \global\@nobreaktrue
         \everypar{\global\@nobreakfalse\everypar{}}%
      \fi
    \endgroup
  \fi}
\newcommand*\l@section[2]{%
  \ifnum \c@tocdepth >\z@
    \addpenalty\@secpenalty
    \addvspace{1.0em \@plus\p@}%
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \bfseries
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\hfil
      \nobreak\hb@xt@\@pnumwidth{\hss #2%
                                 \kern-\p@\kern\p@}\par
    \endgroup
  \fi}
\newcommand*\l@subsection{\@dottedtocline{2}{1.5em}{2.3em}}
\newcommand*\l@subsubsection{\@dottedtocline{3}{3.8em}{3.2em}}
\newcommand*\l@paragraph{\@dottedtocline{4}{7.0em}{4.1em}}
\newcommand*\l@subparagraph{\@dottedtocline{5}{10em}{5em}}
\newcommand\listoffigures{%
    \section*{\listfigurename}%
      \@mkboth{\MakeUppercase\listfigurename}%
              {\MakeUppercase\listfigurename}%
    \@starttoc{lof}%
    }
\newcommand*\l@figure{\@dottedtocline{1}{1.5em}{2.3em}}
\newcommand\listoftables{%
    \section*{\listtablename}%
      \@mkboth{%
          \MakeUppercase\listtablename}%
         {\MakeUppercase\listtablename}%
    \@starttoc{lot}%
    }
\let\l@table\l@figure
\newdimen\bibindent
\setlength\bibindent{1.5em}
%\setlength{\bibsep}{0em}
\newenvironment{thebibliography}[1]
     {\section*{\refname}%
      \@mkboth{\MakeUppercase\refname}{\MakeUppercase\refname}%
      \list{\@biblabel{\@arabic\c@enumiv}}%
           {\settowidth\labelwidth{\@biblabel{#1}}%
            \leftmargin\labelwidth
            \advance\leftmargin\labelsep
            \@openbib@code
            \usecounter{enumiv}%
            \let\p@enumiv\@empty
            \renewcommand\theenumiv{\@arabic\c@enumiv}}%
      \sloppy
      \clubpenalty4000
      \@clubpenalty \clubpenalty
      \widowpenalty4000%
      \sfcode`\.\@m}
     {\def\@noitemerr
       {\@latex@warning{Empty `thebibliography' environment}}%
      \endlist}
\newcommand\newblock{\hskip .11em\@plus.33em\@minus.07em}
\let\@openbib@code\@empty

%\RequirePackage{natbib}  % [super,square,comma,sort&compress]
\usepackage[numbers,square,comma,sort&compress]{natbib} % super,
\setlength{\bibsep}{0em}
%\setlength{\bibhang}{18pt}
\renewcommand{\@biblabel}[1]{[#1]}

\newenvironment{theindex}
               {\if@twocolumn
                  \@restonecolfalse
                \else
                  \@restonecoltrue
                \fi
                \twocolumn[\section*{\indexname}]%
                \@mkboth{\MakeUppercase\indexname}%
                        {\MakeUppercase\indexname}%
                \thispagestyle{plain}\parindent\z@
                \parskip\z@ \@plus .3\p@\relax
                \columnseprule \z@
                \columnsep 35\p@
                \let\item\@idxitem}
               {\if@restonecol\onecolumn\else\clearpage\fi}
\newcommand\@idxitem{\par\hangindent 40\p@}
\newcommand\subitem{\@idxitem \hspace*{20\p@}}
\newcommand\subsubitem{\@idxitem \hspace*{30\p@}}
\newcommand\indexspace{\par \vskip 10\p@ \@plus5\p@ \@minus3\p@\relax}
\renewcommand\footnoterule{%
  \kern-3\p@
  \hrule\@width.1\columnwidth
  \kern2.6\p@}
\newcommand\@makefntext[1]{%
    \parindent 1em%
    \noindent
    \hb@xt@1.8em{\hss\@makefnmark}#1}
\newcommand\contentsname{Contents}
\newcommand\listfigurename{List of Figures}
\newcommand\listtablename{List of Tables}
\renewcommand\refname{References}
\newcommand\indexname{Index}
\newcommand\figurename{Figure}
\newcommand\tablename{Table}
\newcommand\partname{Part}
\newcommand\appendixname{Appendix}
\newcommand\abstractname{Abstract}
\newcommand\keywordsname{Keywords}
\def\today{\ifcase\month\or
  January\or February\or March\or April\or May\or June\or
  July\or August\or September\or October\or November\or December\fi
  \space\number\day, \number\year}
\setlength\columnsep{15\p@}
\setlength\columnseprule{0\p@}
\pagestyle{headings}
\pagenumbering{arabic}
\sloppy
\frenchspacing
% \if@twoside
% \else
%   \raggedbottom
% \fi
% \if@twocolumn
%   \twocolumn
%   \sloppy
%   \flushbottom
% \else
%   \onecolumn
% \fi
\definecolor{green}{cmyk}{0.8,0.02,0.96,0}
\endinput
%%
%% End of file `article.cls'.
