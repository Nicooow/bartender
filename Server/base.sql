--
-- Structure de la table `boisson`
--

CREATE TABLE `boisson` (
  `id` int(11) NOT NULL,
  `nomAffichage` varchar(30) NOT NULL,
  `nomCourt` varchar(30) NOT NULL,
  `couleur` varchar(7) NOT NULL,
  `pourcentageAlcool` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `cuve`
--

CREATE TABLE `cuve` (
  `id` int(11) NOT NULL,
  `idPompe` int(11) NOT NULL,
  `idDebitmetre` int(11) NOT NULL,
  `idBoisson` int(11) NOT NULL,
  `quantitee` float NOT NULL,
  `quantiteemax` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `debitmetre`
--

CREATE TABLE `debitmetre` (
  `id` int(11) NOT NULL,
  `pinId` int(11) NOT NULL,
  `mlParTick` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `pompe`
--

CREATE TABLE `pompe` (
  `id` int(11) NOT NULL,
  `pinId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `boisson`
--
ALTER TABLE `boisson`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `cuve`
--
ALTER TABLE `cuve`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `debitmetre`
--
ALTER TABLE `debitmetre`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `pompe`
--
ALTER TABLE `pompe`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `boisson`
--
ALTER TABLE `boisson`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `cuve`
--
ALTER TABLE `cuve`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `debitmetre`
--
ALTER TABLE `debitmetre`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `pompe`
--
ALTER TABLE `pompe`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE cuve
    ADD CONSTRAINT fk_foreign_debitmetre
    FOREIGN KEY (idDebitmetre)
    REFERENCES debitmetre(id);
    ALTER TABLE cuve
ADD CONSTRAINT fk_foreign_boisson
    FOREIGN KEY (idBoisson)
    REFERENCES boisson(id);
    ALTER TABLE cuve
ADD CONSTRAINT fk_foreign_pompe
    FOREIGN KEY (idPompe)
    REFERENCES pompe(id);
